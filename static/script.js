const input = document.getElementById("user-input");
const sendButton = document.getElementById("send-button");
const movieGrid = document.getElementById("movie-grid");
const loading = document.getElementById("loading");
const subtitle = document.getElementById("recommendation-subtitle");


// ==========================================
// SEND QUERY TO FASTAPI
// ==========================================

async function getRecommendations(query) {

    try {

        // Show loading
        loading.classList.remove("hidden");

        movieGrid.innerHTML = "";

        // Send request to FastAPI
        const response = await fetch("/recommend", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                query: query
            })

        });


        // Check if request was successful
        if (!response.ok) {

            throw new Error("Server error");

        }


        // Convert response to JSON
        const data = await response.json();


        // Display recommendations
        displayMovies(data.recommendations);


        subtitle.textContent =
            `Results for: "${query}"`;

    }

    catch (error) {

        console.error(error);

        movieGrid.innerHTML = `
            <div class="empty-state">

                <div class="empty-icon">⚠️</div>

                <h3>Something went wrong</h3>

                <p>
                    We couldn't get recommendations.
                    Please try again.
                </p>

            </div>
        `;

    }

    finally {

        // Hide loading
        loading.classList.add("hidden");

    }

}


// ==========================================
// DISPLAY MOVIES
// ==========================================

function displayMovies(movies) {

    if (!movies || movies.length === 0) {

        movieGrid.innerHTML = `
            <div class="empty-state">

                <div class="empty-icon">🎬</div>

                <h3>No movies found</h3>

                <p>
                    Try changing your search.
                </p>

            </div>
        `;

        return;
    }


    movieGrid.innerHTML = "";


    movies.forEach((movie, index) => {

        const card = document.createElement("div");

        card.className = "movie-card";


        card.innerHTML = `

            <div class="movie-number">
                #${String(index + 1).padStart(2, "0")}
            </div>

            <h3 class="movie-title">
                ${movie.title}
            </h3>

            <div class="movie-meta">

                <span class="rating">
                    ⭐ ${movie.vote_average}
                </span>

                <span>
                    ${movie.release_year}
                </span>

                ${
                    movie.runtime
                    ? `<span>${movie.runtime} min</span>`
                    : ""
                }

            </div>

            <div class="genre">
                ${formatGenres(movie.genres)}
            </div>

        `;


        movieGrid.appendChild(card);

    });

}


// ==========================================
// FORMAT GENRES
// ==========================================

function formatGenres(genres) {

    if (!genres) {
        return "Movie";
    }


    // If genres arrive as a string
    if (typeof genres === "string") {

        return genres
            .replace(/[\[\]']/g, "")
            .replace(/,/g, " • ");

    }


    // If genres arrive as an array
    if (Array.isArray(genres)) {

        return genres.join(" • ");

    }


    return "Movie";

}


// ==========================================
// SEND BUTTON
// ==========================================

sendButton.addEventListener("click", () => {

    const query = input.value.trim();


    if (!query) {

        input.focus();

        return;

    }


    getRecommendations(query);

});


// ==========================================
// ENTER KEY
// ==========================================

input.addEventListener("keydown", (event) => {

    if (event.key === "Enter") {

        sendButton.click();

    }

});


// ==========================================
// QUICK SUGGESTIONS
// ==========================================

function useSuggestion(text) {

    input.value = text;

    input.focus();

    getRecommendations(text);

}