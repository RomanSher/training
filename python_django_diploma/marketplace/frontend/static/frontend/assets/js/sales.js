var mix = {
    methods: {
        getSales(page = 1) {
            this.getData("/api/sales/", {
                currentPage: page,
            }).then(data => {
                this.salesCards = data.items
                this.currentPage = data.current_page
                this.lastPage = data.last_page
            })
            .catch(() => {
                console.warn('Ошибка при получении товара по скидке')
            })
        },
    },
    mounted() {
        this.getSales();
    },
    data() {
        return {
            salesCards: [],
            currentPage: 1,
            lastPage: 1,
        }
    },
}