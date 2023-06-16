const form = document.forms[0]
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
    avatar.src = contact.avatar
}
    

form.addEventListener('submit', async event => {
    event.preventDefault()

    const response = await fetch(
        `https://SilentDismalSweepsoftware.olieksandrkond3.repl.co/api/contacts/avatar/${contactId}`,
            {
                method: 'PATCH',
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
        avatar.src = result.avatar
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


