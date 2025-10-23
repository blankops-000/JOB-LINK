import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="bg-blue-600 text-white p-4">
      <div className="container mx-auto flex justify-between items-center">
        <Link to="/" className="text-xl font-bold">
          JobLink
        </Link>
        <div className="space-x-4">
          <Link to="/" className="hover:text-blue-200 transition-colors">
            Home
          </Link>
          <Link to="/about" className="hover:text-blue-200 transition-colors">
            About
          </Link>
          <Link to="/services" className="hover:text-blue-200 transition-colors">
            Services
          </Link>
          <Link to="/contact" className="hover:text-blue-200 transition-colors">
            Contact
          </Link>
          <Link to="/login" className="hover:text-blue-200 transition-colors">
            Login
          </Link>
          <Link to="/signup" className="bg-white text-blue-600 px-4 py-2 rounded hover:bg-gray-100 transition-colors">
            Sign Up
          </Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;