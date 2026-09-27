const API = "http://localhost:5000/api";


// ======================================
// REGISTER
// ======================================

const registerForm = document.getElementById("registerForm");

if (registerForm) {

    registerForm.addEventListener("submit", async function (e) {

        e.preventDefault();


        // Get form values
        const name =
            document.getElementById("name").value.trim();

        const email =
            document.getElementById("email").value.trim().toLowerCase();

        const password =
            document.getElementById("password").value;

        const confirmPassword =
            document.getElementById("confirm").value;


        console.log("Password:", password);
        console.log("Confirm Password:", confirmPassword);


        // Check passwords
        if (password !== confirmPassword) {

            document.getElementById("msg").textContent =
                "Passwords do not match";

            return;
        }


        // Minimum password length
        if (password.length < 6) {

            document.getElementById("msg").textContent =
                "Password must be at least 6 characters";

            return;
        }


        document.getElementById("msg").textContent =
            "Creating account...";


        try {

            const response = await fetch(
                `${API}/auth/register`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        name: name,
                        email: email,
                        password: password
                    })
                }
            );


            const data = await response.json();

            console.log("Server response:", data);


            if (!response.ok) {

                throw new Error(
                    data.error || "Registration failed"
                );

            }


            document.getElementById("msg").textContent =
                "Registration successful!";


            // Go to login page
            setTimeout(function () {

                window.location.href = "login.html";

            }, 1000);


        } catch (error) {

            console.error("Registration error:", error);

            document.getElementById("msg").textContent =
                error.message;

        }

    });

}


// ======================================
// LOGIN
// ======================================

const loginForm = document.getElementById("loginForm");

if (loginForm) {

    loginForm.addEventListener("submit", async function (e) {

        e.preventDefault();


        // Get form values
        const email =
            document.getElementById("email").value.trim().toLowerCase();

        const password =
            document.getElementById("password").value;


        document.getElementById("msg").textContent =
            "Logging in...";


        try {

            const response = await fetch(
                `${API}/auth/login`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        email: email,
                        password: password
                    })
                }
            );


            const data = await response.json();

            console.log("Server response:", data);


            if (!response.ok) {

                throw new Error(
                    data.error || "Invalid email or password"
                );

            }


            // Save token and user so other pages can use them
            localStorage.setItem("token", data.token);
            localStorage.setItem("user", JSON.stringify(data.user));


            document.getElementById("msg").textContent =
                "Login successful!";


            window.location.href = "dashboard.html";


        } catch (error) {

            console.error("Login error:", error);

            document.getElementById("msg").textContent =
                error.message;

        }

    });

}