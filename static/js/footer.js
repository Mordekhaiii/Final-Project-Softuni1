// Footer Semua Halaman
  const footer = document.getElementById("footer");
  footer.innerHTML = showFooter();

  function showFooter() {
    return `<div class="container-fluid footer">
            <div class="row justify-content-center">
              <div class="col-12 text-center footer-content">
                <div class="footer-title">
                  <h1 class="fw-bold">Oey<span>Alycia</span> Resto &<span>Cafe.</span></h1>
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
                Created by 
                <a href="https://www.instagram.com/oey_alyciarestocafe/" target="_blank" class="text-warning">Oey <span>Alycia</span> Resto & <span>Cafe</span></a> 
                © 2024 Copyright | All Rights Reserved
              </p>
            </div>
          </div>`;

  }