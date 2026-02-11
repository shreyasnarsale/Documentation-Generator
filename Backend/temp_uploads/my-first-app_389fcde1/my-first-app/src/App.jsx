import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Navbar from "./components/Navbar"
import Body from "./components/Body"
import Footer from "./components/Footer"

function App() {
  return (
    <>
    <style>
      {`
      nav {
          background-color: #222;
          color: white;
          padding: 15px;
          display: flex;
          justify-content: space-between;
          align-items: center;
      }
      ul {
          list-style: none;
          display: flex;
          gap: 15px;
          margin: 0;
          padding: 0;
      }
      li {
          cursor: pointer;
      }
      main {
          padding: 20px;
          min-height: 70vh;
      }

      footer {
          text-align: center;
          padding: 15px;
          background-color: yellow;
      }
      `}
    </style>
    <Navbar/>
    <Body/>
    <Footer/>
    </>
  )
}

export default App
