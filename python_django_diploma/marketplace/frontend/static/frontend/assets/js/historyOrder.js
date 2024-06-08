var mix = {
	methods: {
		getHistoryOrder() {
			this.getData("/api/orders/")
				.then(data => {
					this.orders = data.map(order => ({
						...order,
						deliveryType: order.delivery_type,
						paymentType: order.payment_type,
						fullName: order.full_name,
						totalCost: order.total_cost
					}))
				}).catch(() => {
				this.orders = []
				console.warn('Ошибка при получении списка заказов')
			})
		}
	},
	mounted() {
		this.getHistoryOrder();
	},
	data() {
		return {
			orders: [],
		}
	}
}