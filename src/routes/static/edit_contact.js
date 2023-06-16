const form = document.forms[0]
const inputs = document.getElementsByTagName("input")
const access_token = localStorage.getItem("access_token")
const contactId = localStorage.getItem("contactId")

const getContact = async () => {
    const response = await fetch(
        `https://silentdismalsweepsoftware.olieksandrkond3.repl.co/api/contacts/${contactId}`,
        {
            method: 'GET',
            headers: {
                Authorization: `Bearer ${access_token}`
            }
        }
    )

    const contact = await response.json()
    form.first_name.value = contact.first_name
    form.last_name.value = contact.last_name
    form.birthday.value = contact.birthday
    form.job.value = contact.job
    form.email.value = contact.email
    form.phone.value = contact.phone
}
    

form.addEventListener('submit', async event => {
    event.preventDefault()

    query = ""
    for (input of inputs) {
        if ((!input.required || input.name == "phone") && (input.type == "text" || input.type == "date" || input.type == "email" || input.name == "phone") && input.value) {
            if (input.name == "phone") {
                query = `${query}&${input.name}=${"%2B" + input.value.slice(1)}`
            }
            else {
                query = `${query}&${input.name}=${input.value}`
            }
        }
    }
    console.log("query: ", query)

    const response = await fetch(
        `https://SilentDismalSweepsoftware.olieksandrkond3.repl.co/api/contacts/${contactId}?${query}`,
            {
                method: 'PUT',
                headers: {
                    Authorization: `Bearer ${access_token}`
                },
                body: new FormData(form)
            }
    )

    result = await response.json()
    console.log("response status", response.status)
    console.log("result: ", result)

    if (response.status === 202) {

        form.hidden = true
        detail.innerHTML = "Contact updated"
        buttons.hidden = false
    }
    else {
        form.hidden = true
        buttons.hidden = false
        msg = ""
        for (res of result.detail) {
            msg = msg + res.loc[1] + "-error: " + res.msg + "\n"
        }
        detail.innerHTML = msg + "\n" + result.detail
    }
})

getContact()


