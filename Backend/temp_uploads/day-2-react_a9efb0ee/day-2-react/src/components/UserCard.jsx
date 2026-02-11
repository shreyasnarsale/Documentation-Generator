function UserCard({user}) {
    return (
        <div className="card">
            <img src={user.image} alt="User Avatar" />
            <h3>{user.name}</h3>
            {user.email ? <p>{user.email}</p> : <p style={{color: "red"}}>Email Does not Exist</p>}
        </div>
    )
}

export default UserCard

// reusable component