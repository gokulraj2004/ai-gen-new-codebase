import { Link } from 'react-router-dom';

export const HomePage = () => {
  return (
    <div className="text-center py-12">
      <h1 className="text-4xl font-bold text-gray-900 mb-4">
        Welcome to New Codebase
      </h1>
      <p className="text-lg text-gray-600 mb-8">
        A full-stack application built with React and FastAPI.
      </p>
      <div className="flex justify-center space-x-4">
        <Link
          to="/items"
          className="bg-primary-600 text-white px-6 py-3 rounded-lg hover:bg-primary-700 transition-colors"
        >
          Browse Items
        </Link>
        <Link
          to="/register"
          className="bg-gray-200 text-gray-800 px-6 py-3 rounded-lg hover:bg-gray-300 transition-colors"
        >
          Get Started
        </Link>
      </div>
    </div>
  );
};