async function fetchWeatherData(cityName) {
  try {
    let data;

    if (navigator.onLine) {
      // Fetch data from the API when online
      const response = await fetch(
        `https://weatherappproject.wuaze.com/con.php?city=${cityName}`
      );
      const text = await response.text();
      data = JSON.parse(text);

      if (data.length === 0) {
        // If the city name is incorrect show error
        document.querySelector("#detail-description").textContent = `The city name '${cityName}' is incorrect. Please try again.`;
        document.querySelector("#detail-description").style.color = "red";
        document.querySelector("#detail-description").style.fontWeight = "bold";
        return;
      }
      
      // Save data to local storage
      localStorage.setItem(cityName, JSON.stringify(data));
    } else {
      // Offline: Retrieve from local storage (do NOT try to fetch data from API)
      const storedData = localStorage.getItem(cityName);
      if (storedData) {
        data = JSON.parse(storedData);
      } else {
        document.querySelector("#detail-description").textContent = `No locally stored data available for '${cityName}'. Please connect to the internet.`;
        document.querySelector("#detail-description").style.color = "red";
        document.querySelector("#detail-description").style.fontWeight = "bold";
        return;
      }
    }

    // Display weather information
    document.querySelector("#weather-icon").src = `https://openweathermap.org/img/wn/${data[0].icon}@2x.png`;
    document.querySelector("#weather-main").textContent = data[0].weather_condition;
    document.querySelector("#temperature").textContent = Math.round(data[0].temperature) + "°C";

    dayAndDate(data[0].dt, data[0].timezone);
    document.querySelector("#weather-description").textContent = data[0].weather_description;
    document.querySelector("#location-name").textContent = cityName;
    document.querySelector("#city").textContent = cityName;
    document.querySelector("#detail-description").textContent = `The current weather condition is ${data[0].weather_condition}.`;
    document.querySelector("#humidity").textContent = data[0].humidity + " %";
    document.querySelector("#pressure").textContent = data[0].pressure + " hPa";
    document.querySelector("#wind-speed").textContent = data[0].wind_speed + " m/s";
    document.querySelector("#wind-direction").textContent = data[0].wind_direction + " °";
    
    document.querySelector("#detail-description").style.color = "black";
    document.querySelector("#detail-description").style.fontWeight = "normal";
  } catch (error) {
    console.error("Failed to parse JSON:", error);
    document.querySelector("#detail-description").textContent = "There was an error fetching the data. Please try again later.";
  }
}

// Form submission event listener
document.querySelector("#userForm").addEventListener("submit", function (e) {
  e.preventDefault();
  const cityInput = document.querySelector("#search-box").value;
  if (cityInput !== "") {
    fetchWeatherData(cityInput);
  }
});

// Load default city on page load
document.addEventListener("DOMContentLoaded", function () {
  fetchWeatherData("gadsden");
});

// Calculate and display the day and date
let dayAndDate = (dt, timezone) => {
  let d = new Date(dt * 1000);
  let localDate = new Date(d.getTime() + timezone * 1000);
  let day = localDate.toLocaleString("en-US", { timeZone: "UTC", weekday: "long" });
  let date = localDate.toLocaleDateString("en-US", {
    timeZone: "UTC",
    day: "numeric",
    month: "long",
    year: "numeric",
  });
  document.querySelector("#day").textContent = day;
  document.querySelector("#date").textContent = date;
};
