import { createRoot } from 'react-dom/client'
import React,{ Suspense } from 'react'
import { BrowserRouter as Router, useRoutes } from "react-router-dom";
import routes from '~react-pages'

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
        <Router>
          <Main/>
        </Router>
  )
}


if (import.meta.env.DEV) {
  import('./mock/mocks')
    .then(({ authWorker }) => {
      authWorker.start();
      // profileWorker.start();
    }) 
    .then(() => renderPage())
} else {
  renderPage()
}