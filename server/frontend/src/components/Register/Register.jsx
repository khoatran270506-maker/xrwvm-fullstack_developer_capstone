import React from "react";
import "./Register.css";

const Register = () => {
  const handleSubmit = (event) => {
    event.preventDefault();
    alert("Registration form submitted. Backend registration is not configured yet.");
  };

  return (
    <div className="register_container">
      <h1 className="header">Register</h1>

      <form className="inputs" onSubmit={handleSubmit}>
        <div className="input">
          <label htmlFor="username">Username</label>
          <input
            id="username"
            name="username"
            type="text"
            className="input_field"
            placeholder="Enter username"
            required
          />
        </div>

        <div className="input">
          <label htmlFor="firstName">First Name</label>
          <input
            id="firstName"
            name="firstName"
            type="text"
            className="input_field"
            placeholder="Enter first name"
            required
          />
        </div>

        <div className="input">
          <label htmlFor="lastName">Last Name</label>
          <input
            id="lastName"
            name="lastName"
            type="text"
            className="input_field"
            placeholder="Enter last name"
            required
          />
        </div>

        <div className="input">
          <label htmlFor="email">Email</label>
          <input
            id="email"
            name="email"
            type="email"
            className="input_field"
            placeholder="Enter email"
            required
          />
        </div>

        <div className="input">
          <label htmlFor="password">Password</label>
          <input
            id="password"
            name="password"
            type="password"
            className="input_field"
            placeholder="Enter password"
            required
          />
        </div>

        <div className="submit_panel">
          <button className="submit" type="submit">
            Register
          </button>
        </div>
      </form>
    </div>
  );
};

export default Register;
