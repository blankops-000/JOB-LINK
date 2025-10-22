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
        </div>
      </div>
    </nav>
  );
};

export default Navbar;