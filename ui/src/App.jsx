import { useState, useEffect, useRef } from 'react'
import { login, sendMessage, getHistory } from './api.js'

const LS_TOKEN = 'ar_access_token'

function LoginPage({ onLogin }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const data = await login(email, password)
      localStorage.setItem(LS_TOKEN, data.access_token)
      onLogin(data.access_token)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-wrapper">
      <div className="login-card">
        <h1 className="login-title">Autoresponder</h1>
        <p className="login-subtitle">Войдите или зарегистрируйтесь</p>
        <form onSubmit={handleSubmit} className="login-form">
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            autoFocus
          />
          <input
            type="password"
            placeholder="Пароль"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          {error && <p className="error">{error}</p>}
          <button type="submit" disabled={loading}>
            {loading ? 'Загрузка...' : 'Войти / Зарегистрироваться'}
          </button>
        </form>
        <p className="login-hint">Нет аккаунта? Он создастся автоматически.</p>
      </div>
    </div>
  )
}

function ChatPage({ token, onLogout }) {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [sending, setSending] = useState(false)
  const [historyLoading, setHistoryLoading] = useState(true)
  const bottomRef = useRef(null)

  useEffect(() => {
    getHistory(token)
      .then((data) => {
        const history = data.history.flatMap((m) => [
          { from: 'user', text: m.text },
          { from: 'bot', text: m.response },
        ])
        setMessages(history)
      })
      .catch(() => {})
      .finally(() => setHistoryLoading(false))
  }, [token])

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSend = async (e) => {
    e.preventDefault()
    const text = input.trim()
    if (!text || sending) return

    setInput('')
    setMessages((prev) => [...prev, { from: 'user', text }])
    setSending(true)

    try {
      const data = await sendMessage(token, text)
      setMessages((prev) => [...prev, { from: 'bot', text: data.response }])
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { from: 'bot', text: `Ошибка: ${err.message}`, error: true },
      ])
    } finally {
      setSending(false)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem(LS_TOKEN)
    onLogout()
  }

  return (
    <div className="chat-layout">
      <header className="chat-header">
        <span className="chat-title">Autoresponder</span>
        <button className="logout-btn" onClick={handleLogout}>
          Выйти
        </button>
      </header>

      <div className="chat-messages">
        {historyLoading && (
          <div className="center-msg">Загрузка истории...</div>
        )}
        {!historyLoading && messages.length === 0 && (
          <div className="center-msg">Напишите что-нибудь, чтобы начать!</div>
        )}
        {messages.map((msg, i) => (
          <div key={i} className={`bubble-row ${msg.from}`}>
            <div className={`bubble ${msg.from}${msg.error ? ' bubble-error' : ''}`}>
              {msg.text}
            </div>
          </div>
        ))}
        {sending && (
          <div className="bubble-row bot">
            <div className="bubble bot typing">...</div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <form className="chat-input-area" onSubmit={handleSend}>
        <input
          type="text"
          placeholder="Введите сообщение..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={sending}
          autoFocus
        />
        <button type="submit" disabled={sending || !input.trim()}>
          Отправить
        </button>
      </form>
    </div>
  )
}

export default function App() {
  const [token, setToken] = useState(() => localStorage.getItem(LS_TOKEN))

  if (!token) {
    return <LoginPage onLogin={setToken} />
  }
  return <ChatPage token={token} onLogout={() => setToken(null)} />
}
