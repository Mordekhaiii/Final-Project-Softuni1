// Footer Semua Halaman
const footer = document.getElementById("footer");
footer.innerHTML = showFooter();

function showFooter() {
  return `<div class="container-fluid footer">
            <div class="row justify-content-center">
              <div class="col-12 text-center footer-content">
                <div class="footer-title text-white">
                  <h1 class="fw-bold">Oey Alycia Resto & Cafe.</h1>
                  <ul class="list-unstyled text-uppercase">
                    <li>Open from 10:00 AM - 10:00 PM</li>
                    <li class="mb-3">Bogor - Rancabungur</li>
                  </ul>
                  <span class="me-3">
                    <!-- Instagram icon using Feather -->
                    <i data-feather="instagram"></i> Oey Alycia Resto & Cafe
                  </span>
                  <span>
                    <!-- WhatsApp icon using Feather -->
                    <i data-feather="message-square"></i> +6289658868111
                  </span>
                </div>
              </div>
            </div>
            <div class="text-footer text-white text-center">
              <p class="m-0">
                Created with <i class="fa-solid fa-heart text-danger"></i> by 
                <a href="https://www.instagram.com/oey_alyciarestocafe/" target="_blank" class="text-warning">Oey Alycia Resto & Cafe</a> 
                © 2024 Copyright | All Rights Reserved
              </p>
            </div>
          </div>`;
}
