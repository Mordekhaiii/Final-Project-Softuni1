document.addEventListener("alpine:init", () => {
        Alpine.data("products", () => ({
          items: [
            { id: 1, name: "Robusta Brazil", img: "1.jpg", price: 20000 },
            { id: 2, name: "Arabica Blend", img: "2.jpg", price: 25000 },
            { id: 3, name: "Primo Passo", img: "3.jpg", price: 30000 },
            { id: 4, name: "Coffe Bean", img: "4.jpg", price: 35000 },
            { id: 5, name: "Sumatra Mandheling", img: "5.jpg", price: 40000 },
            { id: 6, name: "Papua Mandheling", img: "1.jpg", price: 45000 },
          ],
        }));

        Alpine.store("cart", {
          items: [],
          total: 0,
          quantity: 0,

          add(newItem) {
            const cartItem = this.items.find((item) => item.id === newItem.id);
            if (!cartItem) {
              this.items.push({ ...newItem, quantity: 1, total: newItem.price });
              this.quantity++;
              this.total += newItem.price;
            } else {
              cartItem.quantity++;
              cartItem.total = cartItem.price * cartItem.quantity;
              this.quantity++;
              this.total += cartItem.price;
            }
          },

          remove(id) {
            const cartItem = this.items.find((item) => item.id === id);

            if (cartItem.quantity > 1) {
              cartItem.quantity--;
              cartItem.total = cartItem.price * cartItem.quantity;
              this.quantity--;
              this.total -= cartItem.price;
            } else {
              this.items = this.items.filter((item) => item.id !== id);
              this.quantity--;
              this.total -= cartItem.price;
            }
          },

          rupiah(number) {
            return new Intl.NumberFormat("id-ID", {
              style: "currency",
              currency: "IDR",
              minimumFractionDigits: 0,
            }).format(number);
          },
        });
      });