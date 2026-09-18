function toggleMenu() {
    const nav = document.querySelector(".nav-links");

    if (nav) {
        nav.classList.toggle("mobile-open");
    }
}


/* Reveal animation */

const observer = new IntersectionObserver(
    (entries) => {
        entries.forEach((entry) => {

            if (entry.isIntersecting) {
                entry.target.classList.add("show");
            }

        });
    },
    {
        threshold: 0.1
    }
);


document
    .querySelectorAll(".speciality-card, .treatment-card, .hospital-card, .detail-box")
    .forEach((element) => {

        element.style.opacity = "0";
        element.style.transform = "translateY(20px)";
        element.style.transition = "all 0.6s ease";

        observer.observe(element);

    });


document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll(".show").forEach((element) => {
        element.style.opacity = "1";
        element.style.transform = "translateY(0)";
    });

});