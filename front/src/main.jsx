import { createRoot } from 'react-dom/client'
import React,{ Suspense } from 'react'
import { BrowserRouter as Router, useRoutes } from "react-router-dom";
import routes from '~react-pages'
import { AuthProvider } from './share/auth';
import './assets/global.css'; 

const root = createRoot(document.getElementById("root"))


const Main = () =>{
    return(
      <Suspense fallback={<p>Loading...</p>}>
        {useRoutes(routes)}
      </Suspense>
    )
}

const renderPage = () => {
  root.render(
    <AuthProvider>
      <Router>
        <Main/>
      </Router>
    </AuthProvider>
  )
}


if (import.meta.env.DEV) {
  import('./mock/mocks')
    .then(({ workers }) => {
      workers.start();
      // profileWorker.start();
    }) 
    .then(() => renderPage())
} else {
  renderPage()
}