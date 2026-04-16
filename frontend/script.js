const API_URL = "http://localhost:8000/hebergements?limit=25000";
const DEFAULT_IMAGE =
  "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=1200&q=80";

const listingsContainer = document.getElementById("listings");
const cityInput = document.getElementById("cityInput");
const travelersInput = document.getElementById("travelers");
const searchForm = document.getElementById("searchForm");
const suggestionsBox = document.getElementById("suggestions");

let listingsData = [];
let availableCities = [];

async function loadListings() {
  try {
    const response = await fetch(API_URL);
    const data = await response.json();

    listingsData = data.map((item) => ({
      id: item.id,
      city: item.commune || "Commune inconnue",
      title: item.nom || "Hébergement sans nom",
      travelers: Number(item.capacite) || 0,
      rating: item.nb_etoiles ? `${item.nb_etoiles}/5` : "Non noté",
      type: item.type_hebergement || "Hébergement",
      classement: item.classement || "Non classé",
      departement: item.departement || "Non renseigné",
      image: DEFAULT_IMAGE
    }));

    availableCities = [...new Set(listingsData.map((listing) => listing.city))]
      .filter(Boolean)
      .sort((a, b) => a.localeCompare(b));

    displayListings(listingsData);
  } catch (error) {
    console.error("Erreur lors du chargement des hébergements :", error);
    listingsContainer.innerHTML = `
      <div class="no-results">
        Impossible de charger les données depuis l’API.
      </div>
    `;
  }
}

function displayListings(listings) {
  listingsContainer.innerHTML = "";

  if (listings.length === 0) {
    listingsContainer.innerHTML = `
      <div class="no-results">
        Aucune annonce ne correspond à votre recherche.
      </div>
    `;
    return;
  }

  listings.forEach((listing) => {
    const card = document.createElement("article");
    card.classList.add("card");

    card.innerHTML = `
      <img src="${listing.image}" alt="${listing.title}">
      <div class="card-content">
        <div class="card-top">
          <span class="card-city">${listing.city}</span>
          <span class="card-rating">⭐ ${listing.rating}</span>
        </div>

        <p class="card-title">${listing.title}</p>
        <p class="card-details"><strong>Type :</strong> ${listing.type}</p>
        <p class="card-details"><strong>Capacité :</strong> ${listing.travelers} personne(s)</p>
        <p class="card-details"><strong>Département :</strong> ${listing.departement}</p>
        <span class="card-badge">${listing.classement}</span>
      </div>
    `;

    listingsContainer.appendChild(card);
  });
}

function filterListings() {
  const cityValue = cityInput.value.trim().toLowerCase();
  const travelersValue = travelersInput.value.trim();

  const filtered = listingsData.filter((listing) => {
    const matchesCity =
      cityValue === "" || listing.city.toLowerCase().includes(cityValue);

    const matchesTravelers =
      travelersValue === "" || listing.travelers >= Number(travelersValue);

    return matchesCity && matchesTravelers;
  });

  displayListings(filtered);
}

function showSuggestions(value) {
  const searchValue = value.trim().toLowerCase();

  if (!searchValue) {
    suggestionsBox.style.display = "none";
    suggestionsBox.innerHTML = "";
    return;
  }

  const filteredCities = availableCities.filter((city) =>
    city.toLowerCase().startsWith(searchValue)
  );

  if (filteredCities.length === 0) {
    suggestionsBox.style.display = "none";
    suggestionsBox.innerHTML = "";
    return;
  }

  suggestionsBox.innerHTML = "";
  suggestionsBox.style.display = "block";

  filteredCities.forEach((city) => {
    const item = document.createElement("div");
    item.classList.add("suggestion-item");
    item.textContent = city;

    item.addEventListener("click", () => {
      cityInput.value = city;
      suggestionsBox.style.display = "none";
      suggestionsBox.innerHTML = "";
      filterListings();
    });

    suggestionsBox.appendChild(item);
  });
}

cityInput.addEventListener("input", () => {
  showSuggestions(cityInput.value);
  filterListings();
});

travelersInput.addEventListener("input", filterListings);

searchForm.addEventListener("submit", (e) => {
  e.preventDefault();
  suggestionsBox.style.display = "none";
  filterListings();
});

document.addEventListener("click", (e) => {
  if (!e.target.closest(".autocomplete-container")) {
    suggestionsBox.style.display = "none";
  }
});

loadListings();