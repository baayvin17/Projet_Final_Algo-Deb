const listingsData = [
  {
    id: 1,
    city: "Paris",
    title: "Appartement cosy au cœur de Paris",
    travelers: 2,
    price: 145,
    rating: 4.8,
    image:
      "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=1200&q=80"
  },
  {
    id: 2,
    city: "Lyon",
    title: "Loft moderne avec vue sur la ville",
    travelers: 4,
    price: 120,
    rating: 4.7,
    image:
      "https://images.unsplash.com/photo-1494526585095-c41746248156?auto=format&fit=crop&w=1200&q=80"
  },
  {
    id: 3,
    city: "Marseille",
    title: "Studio lumineux proche du Vieux-Port",
    travelers: 2,
    price: 95,
    rating: 4.6,
    image:
      "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200&q=80"
  },
  {
    id: 4,
    city: "Bordeaux",
    title: "Maison élégante avec terrasse",
    travelers: 6,
    price: 180,
    rating: 4.9,
    image:
      "https://images.unsplash.com/photo-1448630360428-65456885c650?auto=format&fit=crop&w=1200&q=80"
  },
  {
    id: 5,
    city: "Nice",
    title: "Appartement bord de mer",
    travelers: 3,
    price: 160,
    rating: 4.8,
    image:
      "https://images.unsplash.com/photo-1499793983690-e29da59ef1c2?auto=format&fit=crop&w=1200&q=80"
  },
  {
    id: 6,
    city: "Toulouse",
    title: "Logement chaleureux et spacieux",
    travelers: 5,
    price: 110,
    rating: 4.5,
    image:
      "https://images.unsplash.com/photo-1484154218962-a197022b5858?auto=format&fit=crop&w=1200&q=80"
  }
];

const listingsContainer = document.getElementById("listings");
const cityInput = document.getElementById("cityInput");
const travelersInput = document.getElementById("travelers");
const searchForm = document.getElementById("searchForm");
const suggestionsBox = document.getElementById("suggestions");

const availableCities = [...new Set(listingsData.map(listing => listing.city))];

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
        <p class="card-details">${listing.travelers} voyageurs</p>
        <p class="card-price">${listing.price} € / nuit</p>
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
      suggestionsBox.innerHTML = "";
      suggestionsBox.style.display = "none";
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
  filterListings();
  suggestionsBox.style.display = "none";
});

document.addEventListener("click", (e) => {
  if (!e.target.closest(".autocomplete-container")) {
    suggestionsBox.style.display = "none";
  }
});

displayListings(listingsData);