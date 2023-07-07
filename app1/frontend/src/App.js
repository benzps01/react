import './App.css';
import axios from "axios";
import {format} from "date-fns";
import {useEffect, useState} from "react";

const baseUrl = "http://localhost:5000"

function App() {
  const [description, setDescription] = useState("");
  const [eventsList, setEventsList] = useState([]);

  const fetchEvents = async () => {
    const data = await axios.get(`${baseUrl}/events`)
    const { events } = data.data
    setEventsList(events);
  }

  const handleChange = e => {
    setDescription(e.target.value);
  }

  const handleSubmit = e => {
    e.preventDefault();
    console.log(description);
  }

  useEffect(() => {
    fetchEvents();
  }, [])

  return (
    <div className="App">
      <section>
        <form onSubmit={handleSubmit}>
          <label htmlFor='description'>Description</label>
          <input
            onChange={handleChange}
            type='text'
            name='description'
            id='description'
            value={description}
          />
          <button type="submit">Submit</button>
        </form>
        </section>
        <section>
          <ul>
            {eventsList.map(event => {
              return (
                <li key={event.id}>{event.description}</li>
              )
            })}
          </ul>
        </section>
    </div>
  );
}

export default App;
