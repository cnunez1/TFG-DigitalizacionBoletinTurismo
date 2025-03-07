import { scraper } from "google-maps-review-scraper";
import fs from "fs";

const url = "https://www.google.com/maps/place/Ermita+de+Nuestra+Señora+de+la+Henosa/@41.8994236,-3.8723365,12z/data=!4m16!1m7!3m6!1s0xd467dcaa2a8f4c9:0x22bc67c98aa9d257!2sPunto+Geodésico+(Mirador)!8m2!3d41.8858393!4d-3.8328396!16s%2Fg%2F11k4lh3gf3!3m7!1s0xd467f93314a0cf5:0xb064a02a84a065c1!8m2!3d41.8786372!4d-3.7571186!9m1!1b1!16s%2Fg%2F11_8_zqs9?entry=ttu&g_ep=EgoyMDI1MDMwMy4wIKXMDSoJLDEwMjExNDUzSAFQAw%3D%3D";

(async () => {
  try {
    const reviewsRaw = await scraper(url, { sort_type: "newest", pages: 20, clean: true });

    console.log("Tipo de 'reviewsRaw':", typeof reviewsRaw); 

    const reviews = JSON.parse(reviewsRaw);
    console.log(`Número de reviews: ${reviews.length}`);
    fs.writeFileSync("reviews.json", JSON.stringify(reviews, null, 2), "utf-8");

    console.log("Archivo 'reviews.json' guardado correctamente.");
  } catch (error) {
    console.error("Error al obtener las reviews:", error);
  }
})();
