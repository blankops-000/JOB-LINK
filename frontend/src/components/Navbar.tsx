import { Link } from 'react-router-dom'

const Navbar = () => {
  return (
    <nav className="bg-blue-600 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="text-xl font-bold">
            JobLink
          </Link>
          <div className="flex space-x-8">
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
      </div>
    </nav>
  )
}

export default Navbar