function Navbar() {
    return (
      <nav className="bg-primary p-4 flex items-center justify-between">
        <div className="flex items-center">
          {/* Left Section */}
          <a href="/" className="text-white text-lg font-bold">
            LGO
          </a>
        </div>
  
        {/* Spacer */}
        <div style={{ width: "10%" }}></div>
  
        {/* Right Section */}
        <div className="flex space-x-4">
          <a href="http://localhost:5173/products" className="text-white hover:underline">
            Products
          </a>
          <a href="/" className="text-white hover:underline">
            Kanban
          </a>
        </div>
      </nav>
    );
  }
  
  export default Navbar;
  