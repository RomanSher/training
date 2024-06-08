var mix = {
    methods: {
        submitBasket () {
            this.postData('/api/orders/', Object.values(this.basket))
                .then(({data: { id }}) => {
                    location.assign(`/order/${ id }/`)
                }).catch(() => {
                    console.warn('Ошибка при создании заказа')
                })
        }
    },
    mounted() {},
    data() {
        return {}
    }
}