const fullRefundInput = document.getElementById('id_full_refund')
const refundAmountInput = document.getElementById('id_amount')
const refundReasonInput = document.getElementById('id_reason')
const refundBtn = document.getElementById('refund_btn')
const totalRefundElement = document.getElementById('total_refund')
const orderRefundListElement = document.getElementById('orderRefundList')
const deliveryForm = document.getElementById('delivery-form')
const refundForm = document.getElementById('refund-form')
const deliveryLogHistoryElement = document.getElementById('order_delivery_logs')

refundForm.addEventListener('submit', async (event) => {
  event.preventDefault()
  refundBtn.disabled = true

  const formData = new FormData(event.currentTarget);

  try {
    const response = await fetch(`/api/orders/${orderId}/refund`, {
      method: 'POST',
      body: formData,
      headers: { "X-CSRFToken": csrftoken },
    });

    const data = await response.json()

    if (response.ok) {
      successAlert(data.message)
      handleRefundSuccess(data)
      refundBtn.disabled = false
    } else{
      throw new Error(JSON.stringify(data))
    }
  } catch (error) {
    refundBtn.disabled = false
    errorAlert(JSON.parse(error.message)?.message)
    handleRefundErrors(JSON.parse(error.message).errors)
  }
})

deliveryForm.addEventListener('submit', async (event) => {
  event.preventDefault()
  const formData = new FormData(event.currentTarget);

  try {
    const response = await fetch(`/api/orders/${orderId}/update-delivery`, {
      method: 'POST',
      body: formData,
      headers: { "X-CSRFToken": csrftoken },
    });

    const data = await response.json()

    if (response.ok) {
      successAlert(data.message)
      if(data?.delivery_log?.history_change_reason){
        handleDeliverySuccess(data)
      }
    } else{
      throw new Error(JSON.stringify(data))
    }
  } catch (error) {
    refundBtn.disabled = false
    console.log(error)
    if(error.message){
      errorAlert(JSON.parse(error.message)?.message)
      handleDeliveryErrors(JSON.parse(error.message)?.errors)
    }
  }
})

function handleRefundSuccess(data){
  for (const field in deliveryForm.elements) {
    deliveryForm.elements[field]?.classList?.remove('is-invalid')
  }
  refundAmountInput.value = ''
  refundReasonInput.value = ''
  totalRefundElement.innerHTML = data.order.total_refund
  orderRefundListElement.innerHTML = refundComponent(data.order_refund) + orderRefundListElement.innerHTML
}

function handleRefundErrors(errors){
  for (const field in errors) {
    document.getElementById(`id_${field}`).classList.add('is-invalid')
    document.getElementById(`id_${field}_errors`).innerHTML = errors[field].join('\n')
  }
}

function handleDeliverySuccess(data){
  for (const field in deliveryForm.elements) {
    deliveryForm.elements[field]?.classList?.remove('is-invalid')
  }
  deliveryLogHistoryElement.innerHTML = logComponent(data.delivery_log) + deliveryLogHistoryElement.innerHTML
}

function handleDeliveryErrors(errors){
  for (const field in errors) {
    document.getElementById(`id_${field}`).classList.add('is-invalid')
    document.getElementById(`id_${field}_errors`).innerHTML = errors[field].join('\n')
  }
}

function logComponent(log){
  return `<li class="list-group-item d-flex justify-content-between align-items-start">
    <div class="ms-2 me-auto">
        <small class="d-block text-muted">
            ${log?.history_change_reason}
        </small>
        <small class="d-block">            
            ${log?.history_user}
        </small>
    </div>
    <span class="badge bg-primary rounded-pill">${log?.history_date}</span>
  </li>`
}

fullRefundInput.addEventListener('change', (event) => {
  if (event.currentTarget.checked) {
    document.getElementById('refund_amount').classList.add('d-none')
    refundBtn.disabled = false
    refundBtn.classList.remove('btn-disabled')
  } else {
    document.getElementById('refund_amount').classList.remove('d-none')
    if (event.currentTarget.value <= Number(orderTotalPaid) - Number(orderTotalRefund)) {
      refundBtn.disabled = false
      refundBtn.classList.remove('btn-disabled')
    } else {
      refundBtn.disabled = true
      refundBtn.classList.add('btn-disabled')
    }
  }
})

refundAmountInput.addEventListener('input', (event) => {
  const amount = event.currentTarget.value
  validateRefundAmount(amount)
})

function validateRefundAmount(amount) {
  if (amount && amount !== '' && amount !== 'NaN' && amount <= Number(orderTotalPaid) - Number(orderTotalRefund)) {
    refundBtn.disabled = false
    refundBtn.classList.remove('btn-disabled')
    document.getElementById('refundAmountHelp').classList.remove('invalid-feedback')
    refundAmountInput.classList.remove('is-invalid')
  } else {
    refundBtn.disabled = true
    refundBtn.classList.add('btn-disabled')
    document.getElementById('refundAmountHelp').classList.add('invalid-feedback')
    refundAmountInput.classList.add('is-invalid')
  }
}

function refundComponent(refund) {
  return `<li class="list-group-item list-group-item-action">
    <div class="d-flex w-100 justify-content-between">
      <h6 class="mb-1">${refund.amount} &#8380;</h6>
      <small>${refund.created_date}</small>
    </div>
    <p class="mb-1">${refund.created_by_name}</p>
    <small>${refund.reason}</small>
  </li>`
}