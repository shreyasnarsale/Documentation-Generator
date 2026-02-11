import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import UserCard from './components/UserCard'

function App() {

  const users = [
    {
      id: 1,
      image: "https://via.placeholder.com/100",
      name: "John Doe",
      email: "john.doe@example.com",
    },
    {
      id: 2,
      image: "https://via.placeholder.com/100",
      name: "Jane Smith",
      email: null,
    },
    {
      id: 3,
      image: "https://via.placeholder.com/100",
      name: "Alice Johnson",
      email: "alice.johnson@example.com",
    },
  ];

  return (
    <>
      {users.map((user)=>(
        <UserCard key={user.id} user={user}/>
      ))}
    </>
  )
}

export default App
