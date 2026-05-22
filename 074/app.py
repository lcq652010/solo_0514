from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

STEPS = ['选纸', '裱扇', '绘图', '题字', '上胶', '晾干', '完工']
CATEGORY_CODE = 'FS'
INSCRIPTION_MAX_LENGTH = 50

def sanitize_inscription(text):
    if not text:
        return ''
    text = text.strip()
    text = re.sub(r'[<>"\'\\]', '', text)
    text = re.sub(r'[^\w\s\u4e00-\u9fff，。！？、；：""''（）【】《》!.,;?]', '', text)
    if len(text) > INSCRIPTION_MAX_LENGTH:
        text = text[:INSCRIPTION_MAX_LENGTH]
    return text

def validate_inscription(text):
    if not text:
        return True, ''
    if len(text) > INSCRIPTION_MAX_LENGTH:
        return False, f'题字内容不能超过{INSCRIPTION_MAX_LENGTH}字'
    if re.search(r'[<>"\'\\]', text):
        return False, '题字内容包含非法字符'
    return True, ''

def generate_order_number():
    now = datetime.now()
    year_month = now.strftime('%Y%m')
    
    max_attempts = 10
    for attempt in range(max_attempts):
        last_order = Order.query.filter(
            Order.order_number.like(f'{year_month}{CATEGORY_CODE}%')
        ).order_by(Order.id.desc()).first()
        
        if last_order:
            try:
                last_num = int(last_order.order_number[-4:])
                new_num = last_num + 1
            except (ValueError, IndexError):
                new_num = 1
        else:
            new_num = 1
        
        serial_number = f'{new_num:04d}'
        order_number = f'{year_month}{CATEGORY_CODE}{serial_number}'
        
        existing = Order.query.filter_by(order_number=order_number).first()
        if not existing:
            return order_number
        
        app.logger.warning(f'订单号冲突，正在重试... 尝试次数: {attempt + 1}')
    
    timestamp = now.strftime('%H%M%S')
    return f'{year_month}{CATEGORY_CODE}{timestamp}'

class ProcessHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    old_step = db.Column(db.Integer, nullable=False)
    new_step = db.Column(db.Integer, nullable=False)
    operator = db.Column(db.String(50), default='管理员')
    operation_type = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    remark = db.Column(db.String(200))

    order = db.relationship('Order', backref=db.backref('process_history', lazy=True))

    def get_old_step_name(self):
        return STEPS[self.old_step] if 0 <= self.old_step < len(STEPS) else '未知'
    
    def get_new_step_name(self):
        return STEPS[self.new_step] if 0 <= self.new_step < len(STEPS) else '未知'

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True, nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    paper_type = db.Column(db.String(50), nullable=False)
    paper_model = db.Column(db.String(50), nullable=False)
    fan_size = db.Column(db.String(50), nullable=False)
    fan_bone_size = db.Column(db.String(50), nullable=False)
    theme = db.Column(db.String(100), nullable=False)
    design_description = db.Column(db.Text, nullable=False)
    inscription = db.Column(db.String(200))
    current_step = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def get_progress(self):
        return STEPS[:self.current_step + 1]

    def get_remaining_steps(self):
        return STEPS[self.current_step + 1:]

    def can_advance_to(self, target_step):
        return target_step == self.current_step + 1

    def can_regress_to(self, target_step):
        return target_step >= 0 and target_step <= self.current_step
    
    def get_sorted_history(self):
        return sorted(self.process_history, key=lambda x: x.created_at, reverse=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/order', methods=['GET', 'POST'])
def create_order():
    if request.method == 'POST':
        inscription = request.form.get('inscription', '')
        
        valid, msg = validate_inscription(inscription)
        if not valid:
            flash(msg, 'error')
            return redirect(url_for('create_order'))
        
        sanitized_inscription = sanitize_inscription(inscription)
        
        order_number = generate_order_number()
        
        order = Order(
            order_number=order_number,
            customer_name=request.form['customer_name'],
            phone=request.form['phone'],
            address=request.form['address'],
            paper_type=request.form['paper_type'],
            paper_model=request.form['paper_model'],
            fan_size=request.form['fan_size'],
            fan_bone_size=request.form['fan_bone_size'],
            theme=request.form['theme'],
            design_description=request.form['design_description'],
            inscription=sanitized_inscription
        )
        
        db.session.add(order)
        try:
            db.session.commit()
            
            history = ProcessHistory(
                order_id=order.id,
                old_step=-1,
                new_step=0,
                operation_type='创建订单',
                remark='订单创建成功，初始状态：选纸'
            )
            db.session.add(history)
            db.session.commit()
            
            flash(f'订单提交成功！您的订单号是：{order_number}')
            return redirect(url_for('order_detail', order_number=order_number))
        except Exception as e:
            db.session.rollback()
            app.logger.error(f'创建订单失败: {str(e)}')
            flash('订单创建失败，请重试', 'error')
            return redirect(url_for('create_order'))
    
    paper_types = ['生宣', '熟宣', '半生熟宣', '皮纸', '麻纸']
    paper_models = ['四尺', '六尺', '八尺', '丈二', '斗方', '扇面专用']
    fan_sizes = ['7寸(23cm)', '8寸(27cm)', '9寸(30cm)', '10寸(33cm)', '12寸(40cm)']
    fan_bone_sizes = ['15方', '18方', '20方', '22方', '24方', '30方']
    themes = ['山水', '花鸟', '人物', '书法', '工笔', '写意', '仿古', '现代']
    return render_template('create_order.html', 
                         paper_types=paper_types,
                         paper_models=paper_models,
                         fan_sizes=fan_sizes,
                         fan_bone_sizes=fan_bone_sizes,
                         themes=themes,
                         max_inscription_length=INSCRIPTION_MAX_LENGTH)

@app.route('/order/<order_number>')
def order_detail(order_number):
    order = Order.query.filter_by(order_number=order_number).first_or_404()
    return render_template('order_detail.html', order=order, steps=STEPS)

@app.route('/admin')
def admin():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin.html', orders=orders, steps=STEPS)

@app.route('/admin/<order_number>/update', methods=['POST'])
def update_progress(order_number):
    order = Order.query.filter_by(order_number=order_number).first_or_404()
    new_step = int(request.form['current_step'])
    old_step = order.current_step
    
    if 0 <= new_step < len(STEPS):
        if new_step > old_step:
            if order.can_advance_to(new_step):
                order.current_step = new_step
                operation_type = '进度推进'
                remark = f'从「{STEPS[old_step]}」推进到「{STEPS[new_step]}」'
                
                history = ProcessHistory(
                    order_id=order.id,
                    old_step=old_step,
                    new_step=new_step,
                    operation_type=operation_type,
                    remark=remark
                )
                db.session.add(history)
                db.session.commit()
                
                flash(f'订单 {order_number} {remark}')
            else:
                flash(f'错误：工序不可跳步！当前为「{STEPS[old_step]}」，下一步应为「{STEPS[old_step + 1]}」', 'error')
        elif new_step < old_step:
            if order.can_regress_to(new_step):
                order.current_step = new_step
                operation_type = '进度回退'
                remark = f'从「{STEPS[old_step]}」回退到「{STEPS[new_step]}」'
                
                history = ProcessHistory(
                    order_id=order.id,
                    old_step=old_step,
                    new_step=new_step,
                    operation_type=operation_type,
                    remark=remark
                )
                db.session.add(history)
                db.session.commit()
                
                flash(f'订单 {order_number} {remark}')
            else:
                flash('错误：无效的工序回退操作', 'error')
    else:
        flash('错误：无效的工序序号', 'error')
    
    return redirect(url_for('admin'))

@app.route('/search', methods=['GET', 'POST'])
def search_order():
    order = None
    if request.method == 'POST':
        order_number = request.form['order_number'].strip()
        order = Order.query.filter_by(order_number=order_number).first()
        if not order:
            flash('未找到该订单，请检查订单号是否正确', 'error')
    return render_template('search.html', order=order, steps=STEPS)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
