const API_URL = "http://localhost:8000/hebergements?limit=25000";
const DEFAULT_IMAGE =
  "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=1200&q=80";

const listingsContainer = document.getElementById("listings");
const cityInput = document.getElementById("cityInput");
const travelersInput = document.getElementById("travelers");
const searchForm = document.getElementById("searchForm");
const suggestionsBox = document.getElementById("suggestions");

let listingsData = [];
let filteredData = [];
let availableCities = [];
let currentPage = 1;
let pageSize = 50;

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

    filteredData = listingsData;
    currentPage = 1;
    renderPage();
  } catch (error) {
    console.error("Erreur lors du chargement des hébergements :", error);
    listingsContainer.innerHTML = `
      <div class="no-results">
        Impossible de charger les données depuis l'API.
      </div>
    `;
  }
}

function renderPage() {
  listingsContainer.innerHTML = "";

  removePagination();

  if (filteredData.length === 0) {
    listingsContainer.innerHTML = `
      <div class="no-results">
        Aucune annonce ne correspond à votre recherche.
      </div>
    `;
    return;
  }

  const totalPages = Math.ceil(filteredData.length / pageSize);
  if (currentPage > totalPages) currentPage = totalPages;

  const start = (currentPage - 1) * pageSize;
  const end = start + pageSize;
  const pageItems = filteredData.slice(start, end);

  pageItems.forEach((listing) => {
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

  renderPagination(totalPages);
}

function renderPagination(totalPages) {
  const mainContent = document.querySelector(".main-content");

  const wrapper = document.createElement("div");
  wrapper.classList.add("pagination-wrapper");

  const info = document.createElement("div");
  info.classList.add("pagination-info");
  const start = (currentPage - 1) * pageSize + 1;
  const end = Math.min(currentPage * pageSize, filteredData.length);
  info.textContent = `${start}–${end} sur ${filteredData.length} hébergements`;

  const controls = document.createElement("div");
  controls.classList.add("pagination-controls");

  const prevBtn = document.createElement("button");
  prevBtn.classList.add("pagination-btn");
  prevBtn.textContent = "← Précédent";
  prevBtn.disabled = currentPage === 1;
  prevBtn.addEventListener("click", () => {
    if (currentPage > 1) {
      currentPage--;
      renderPage();
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  });

  const pageNumbers = buildPageNumbers(totalPages);

  const nextBtn = document.createElement("button");
  nextBtn.classList.add("pagination-btn");
  nextBtn.textContent = "Suivant →";
  nextBtn.disabled = currentPage === totalPages;
  nextBtn.addEventListener("click", () => {
    if (currentPage < totalPages) {
      currentPage++;
      renderPage();
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  });

  controls.appendChild(prevBtn);
  controls.appendChild(pageNumbers);
  controls.appendChild(nextBtn);

  const sizeSelector = document.createElement("div");
  sizeSelector.classList.add("page-size-selector");

  const sizeLabel = document.createElement("label");
  sizeLabel.textContent = "Afficher :";
  sizeLabel.setAttribute("for", "pageSizeSelect");

  const sizeSelect = document.createElement("select");
  sizeSelect.id = "pageSizeSelect";
  [25, 50, 100, 200].forEach((size) => {
    const option = document.createElement("option");
    option.value = size;
    option.textContent = `${size} / page`;
    if (size === pageSize) option.selected = true;
    sizeSelect.appendChild(option);
  });

  sizeSelect.addEventListener("change", () => {
    pageSize = Number(sizeSelect.value);
    currentPage = 1;
    renderPage();
  });

  sizeSelector.appendChild(sizeLabel);
  sizeSelector.appendChild(sizeSelect);

  wrapper.appendChild(info);
  wrapper.appendChild(controls);
  wrapper.appendChild(sizeSelector);

  mainContent.appendChild(wrapper);
}

function buildPageNumbers(totalPages) {
  const container = document.createElement("div");
  container.classList.add("pagination-pages");

  const range = getPaginationRange(currentPage, totalPages);

  range.forEach((item) => {
    if (item === "…") {
      const ellipsis = document.createElement("span");
      ellipsis.classList.add("pagination-ellipsis");
      ellipsis.textContent = "…";
      container.appendChild(ellipsis);
    } else {
      const btn = document.createElement("button");
      btn.classList.add("pagination-page");
      if (item === currentPage) btn.classList.add("active");
      btn.textContent = item;
      btn.addEventListener("click", () => {
        currentPage = item;
        renderPage();
        window.scrollTo({ top: 0, behavior: "smooth" });
      });
      container.appendChild(btn);
    }
  });

  return container;
}

function getPaginationRange(current, total) {
  if (total <= 7) return Array.from({ length: total }, (_, i) => i + 1);

  const pages = [];

  pages.push(1);

  if (current > 3) pages.push("…");

  for (let i = Math.max(2, current - 1); i <= Math.min(total - 1, current + 1); i++) {
    pages.push(i);
  }

  if (current < total - 2) pages.push("…");

  pages.push(total);

  return pages;
}

function removePagination() {
  const existing = document.querySelector(".pagination-wrapper");
  if (existing) existing.remove();
}

function filterListings() {
  const cityValue = cityInput.value.trim().toLowerCase();
  const travelersValue = travelersInput.value.trim();

  filteredData = listingsData.filter((listing) => {
    const matchesCity =
      cityValue === "" || listing.city.toLowerCase().includes(cityValue);
    const matchesTravelers =
      travelersValue === "" || listing.travelers >= Number(travelersValue);
    return matchesCity && matchesTravelers;
  });

  currentPage = 1;
  renderPage();
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