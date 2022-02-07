import logo from './logo.svg';
import './App.css';
import RealMap from './RealMap';

function App() {
  return (
    <div className="App">
      <nav className="navbar navbar-light bg-light">
        <div className="container-fluid">
          <a className="navbar-brand">CSE557A Project 2</a>
          <form className="d-flex">
          <input className="form-control me-2" type="search" placeholder="Search" aria-label="Search"/>
            <button className="btn btn-outline-success" type="submit">Search</button>
          </form>
        </div>
      </nav>
      
    <div className="container">
        <div className="row justify-content-md-center">
            <div className="col-2">
                <select className="form-select" aria-label="Default select example">
                    <option selected>Open this select menu</option>
                    <option value="1">One</option>
                    <option value="2">Two</option>
                    <option value="3">Three</option>
                  </select>                  
            </div>
            <div className="col-10">
            <RealMap/>
            </div>
      </div>
    </div>
  </div>
  );
}

export default App;
