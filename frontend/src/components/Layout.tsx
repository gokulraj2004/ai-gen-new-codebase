import { Outlet, Link } from 'react-router-dom';

export const Layout = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-primary-600 text-white shadow-md">
        <nav className="container mx-auto px-4 py-4 flex items-center justify-between">
          <Link to="/" className="text-xl font-bold">
            New Codebase
          </Link>
          <div className="flex items-center space-x-4">
            <Link to="/items" className="hover:text-primary-200 transition-colors">
              Items
            </Link>
            <Link to="/login" className="hover:text-primary-200 transition-colors">
              Login
            </Link>
            <Link to="/register" className="hover:text-primary-200 transition-colors">
              Register
            </Link>
            <Link to="/profile" className="hover:text-primary-200 transition-colors">
              Profile
            </Link>
          </div>
        </nav>
      </header>
      <main className="flex-1 container mx-auto px-4 py-8">
        <Outlet />
      </main>
      <footer className="bg-gray-100 border-t py-4">
        <div className="container mx-auto px-4 text-center text-gray-600">
          &copy; {new Date().getFullYear()} New Codebase. All rights reserved.
        </div>
      </footer>
    </div>
  );
};