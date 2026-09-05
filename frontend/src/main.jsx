import { useState } from 'react'
import { createRoot } from 'react-dom/client'
import {
  ArrowUpRight,
  BookOpen,
  ChevronDown,
  ChevronRight,
  CircleHelp,
  Clock3,
  Code2,
  FileCode2,
  Folder,
  GitBranch,
  Layers3,
  LockKeyhole,
  MessageSquareText,
  MoreHorizontal,
  Search,
  Send,
  Settings2,
  Sparkles,
  TerminalSquare,
  UploadCloud,
  X,
} from 'lucide-react'
import './styles.css'

const files = [
  { name: 'app', type: 'folder', open: true },
  { name: 'api', type: 'folder', indent: 1, open: true },
  { name: 'router.py', type: 'python', indent: 2, active: true },
  { name: 'routes.py', type: 'python', indent: 2 },
  { name: 'main.py', type: 'python', indent: 1 },
  { name: 'config', type: 'folder', indent: 1 },
  { name: 'settings.py', type: 'python', indent: 2 },
  { name: 'ingestion', type: 'folder', indent: 1 },
  { name: 'chunker.py', type: 'python', indent: 2 },
  { name: 'README.md', type: 'markdown' },
]

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

function App() {
  const [question, setQuestion] = useState('How does the ingestion pipeline split and store documents?')
  const [submittedQuestion, setSubmittedQuestion] = useState('')
  const [answer, setAnswer] = useState('')
  const [repositoryUrl, setRepositoryUrl] = useState('')
  const [repositoryName, setRepositoryName] = useState('No repository indexed')
  const [filesIndexed, setFilesIndexed] = useState(0)
  const [isIndexing, setIsIndexing] = useState(false)
  const [isAsking, setIsAsking] = useState(false)
  const [error, setError] = useState('')

  async function connectRepository() {
    const githubUrl = window.prompt('Enter a public GitHub repository URL')
    if (!githubUrl?.trim()) return

    setIsIndexing(true)
    setError('')
    try {
      const response = await fetch(`${API_BASE_URL}/index`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ github_url: githubUrl.trim() }),
      })
      const data = await response.json()
      if (!response.ok) throw new Error(data.detail || data.message || 'Repository indexing failed.')
      setRepositoryUrl(githubUrl.trim())
      setRepositoryName(data.repository)
      setFilesIndexed(data.files_loaded)
      setAnswer('')
    } catch (requestError) {
      setError(requestError.message)
    } finally {
      setIsIndexing(false)
    }
  }

  async function askQuestion(event) {
    event.preventDefault()
    if (!question.trim()) return

    setIsAsking(true)
    setError('')
    setSubmittedQuestion(question.trim())
    try {
      const response = await fetch(`${API_BASE_URL}/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: question.trim() }),
      })
      const data = await response.json()
      if (!response.ok) throw new Error(data.detail || 'The question could not be answered.')
      setAnswer(data.answer || 'The API returned no answer.')
      if (data.repository) setRepositoryName(data.repository)
    } catch (requestError) {
      setError(requestError.message)
      setAnswer('')
    } finally {
      setIsAsking(false)
    }
  }

  return (
    <main className="app-shell">
      <aside className="sidebar">
        <div className="brand"><div className="brand-mark"><Code2 size={19} strokeWidth={2.6} /></div><span>Code Query</span><small>code rag</small></div>
        <button className="workspace-switcher"><span className="repo-dot" />Summify <ChevronDown size={15} /></button>
        <nav className="nav-list">
          <div className="nav-label">workspace</div>
          <a className="nav-item active"><Layers3 size={17} />Overview</a>
          <a className="nav-item"><MessageSquareText size={17} />Ask your code<span className="nav-count">3</span></a>
          <a className="nav-item"><FileCode2 size={17} />Indexed files</a>
          <div className="nav-label spaced">manage</div>
          <a className="nav-item"><GitBranch size={17} />Repositories</a>
          <a className="nav-item"><Clock3 size={17} />Activity</a>
        </nav>
        <div className="sidebar-bottom">
          <div className="usage-label"><span>index capacity</span><b>68%</b></div>
          <div className="usage-bar"><span /></div>
          <p>14,208 of 20,000 chunks</p>
          <a className="nav-item"><Settings2 size={17} />Settings</a>
          <div className="user-card"><div className="avatar">SJ</div><div><strong>Suchay Joshi</strong><span>Personal workspace</span></div><MoreHorizontal size={17} /></div>
        </div>
      </aside>

      <section className="main-content">
        <header className="topbar">
          <div className="breadcrumbs"><span>Workspace</span><ChevronRight size={14} /><strong>Overview</strong></div>
          <div className="top-actions"><span className="sync-status"><span /> Synced 8 min ago</span><button className="icon-button" title="Help"><CircleHelp size={18} /></button><button className="avatar small">SJ</button></div>
        </header>

        <div className="content-wrap">
          <div className="page-heading"><div><p className="eyebrow">Repository intelligence / 01</p><h1>Good morning, Suchay<span className="accent">.</span></h1><p className="subheading">A clear view into what Code Query knows about your codebase.</p></div><button className="outline-button" onClick={connectRepository} disabled={isIndexing}>{isIndexing ? 'Indexing...' : <><GitBranch size={16} />{repositoryUrl ? 'Re-index repository' : 'Connect repository'}</>}</button></div>

          <section className="stats-grid">
            <article className="stat-card highlight"><div className="stat-icon"><Sparkles size={18} /></div><span className="stat-label">Repository health</span><strong>Excellent</strong><small><span className="positive">↑ 12%</span> from last index</small><div className="health-lines"><i /><i /><i /><i /><i /><i /><i /><i /><i /><i /><i /><i /></div></article>
            <article className="stat-card"><div className="stat-top"><span className="stat-label">Files indexed</span><FileCode2 size={18} /></div><strong>{filesIndexed.toLocaleString()}</strong><small>{repositoryUrl ? 'from the active repository' : 'index a repository to begin'}</small><div className="mini-bars"><i /><i /><i /><i /><i /><i /><i /><i /><i /></div></article>
            <article className="stat-card"><div className="stat-top"><span className="stat-label">Last indexed</span><Clock3 size={18} /></div><strong>8 min ago</strong><small>842 files changed</small><div className="activity-dots"><i /><i /><i /><i /><i /><i /><i /><i /><i /><i /><i /><i /><i /><i /></div></article>
          </section>

          <div className="dashboard-grid">
            <section className="panel ask-panel"><div className="panel-heading"><div><p className="eyebrow">Ask the codebase</p><h2>What do you want to understand?</h2></div><div className="ai-badge"><Sparkles size={14} /> grounded AI</div></div>
              <form className="question-box" onSubmit={askQuestion}><textarea value={question} onChange={(e) => setQuestion(e.target.value)} rows="3" /><div className="question-toolbar"><span><LockKeyhole size={14} /> Answers use indexed code only</span><button className="send-button" type="submit" disabled={isAsking}>{isAsking ? 'Asking...' : <><Send size={16} /> Ask Code Query</>}</button></div></form>
              {error && <p className="api-error">{error}</p>}
              <div className="answer-block">{answer ? <><div className="answer-meta"><div className="answer-avatar"><Sparkles size={15} /></div><span>Code Query answered from {repositoryName}</span><time>just now</time><button className="plain-icon" title="More"><MoreHorizontal size={17} /></button></div><h3>{submittedQuestion}</h3>{answer.split('\n').filter(Boolean).map((paragraph) => <p className="answer-copy" key={paragraph}>{paragraph}</p>)}</> : <p className="answer-copy">Index a public GitHub repository, then ask a question to receive an answer grounded in its code.</p>}</div>
            </section>

            <aside className="right-rail"><section className="panel repository-panel"><div className="panel-heading compact"><div><p className="eyebrow">Active repository</p><h2><span className="repo-dot" />{repositoryName}</h2></div><button className="plain-icon" title="Repository menu"><MoreHorizontal size={18} /></button></div><div className="repo-url"><GitBranch size={15} /> {repositoryUrl || 'No repository connected'} </div><div className="repo-stats"><div><strong>{filesIndexed.toLocaleString()}</strong><span>documents</span></div><div><strong>{repositoryUrl ? 'ready' : 'idle'}</strong><span>status</span></div><div><strong>API</strong><span>source</span></div></div><button className="text-button" onClick={connectRepository}>Index a repository <ArrowUpRight size={15} /></button></section>
              <section className="panel files-panel"><div className="panel-heading compact"><div><p className="eyebrow">Source explorer</p><h2>Indexed files</h2></div><button className="plain-icon"><Search size={17} /></button></div><div className="file-search"><Search size={15} /><input placeholder="Filter files" /></div><div className="file-tree">{files.map((file) => <div className={`file-row ${file.active ? 'selected' : ''}`} key={`${file.indent}-${file.name}`} style={{ paddingLeft: `${14 + (file.indent || 0) * 17}px` }}>{file.type === 'folder' ? <Folder size={15} fill="currentColor" /> : file.type === 'markdown' ? <BookOpen size={15} /> : <TerminalSquare size={15} />}<span>{file.name}</span>{file.type === 'folder' && <ChevronDown className="folder-chevron" size={13} />}</div>)}</div><button className="browse-button">Browse all files <ArrowUpRight size={14} /></button></section>
            </aside>
          </div>

          <section className="activity-strip"><div className="activity-title"><div className="strip-icon"><UploadCloud size={17} /></div><div><strong>Indexing is healthy</strong><span>Next automatic sync in 52 minutes</span></div></div><div className="activity-progress"><div className="progress-label"><span>Current progress</span><b>100%</b></div><div className="progress-track"><span /></div></div><button className="plain-icon"><X size={16} /></button></section>
        </div>
      </section>
    </main>
  )
}

export default App

createRoot(document.getElementById('root')).render(<App />)
