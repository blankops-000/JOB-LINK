const Home = () => {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-800 mb-4">
          Welcome to JobLink
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Connecting everyday people to reliable local service providers
        </p>
        <button className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition-colors">
          Find Services
        </button>
      </div>
    </div>
  )
}

export default Home