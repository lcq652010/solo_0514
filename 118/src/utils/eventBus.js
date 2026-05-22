import Vue from 'vue'
export const EventBus = new Vue()
export const playNewOrderSound = () => {
  const speech = new SpeechSynthesisUtterance()
  speech.text = '您有新的订单，请及时处理'
  speech.lang = 'zh-CN'
  speech.volume = 1
  speech.rate = 1
  speech.pitch = 1
  window.speechSynthesis.speak(speech)
}
