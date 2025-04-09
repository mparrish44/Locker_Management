function getUserLocker() {
    const token = localStorage.getItem('access_token');
    fetch('/users/locker', {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    }).then(response => response.json())
    .then(data => {
        document.getElementById('lockerInfo').innerHTML = `
            <p>Building: ${data.building_name}</p>
            <p>Locker Number: ${data.locker_number}</p>
        `;
    }).catch(error => {
        document.getElementById('lockerInfo').innerHTML = `<p>Error: ${error.message}</p>`;
    });
}

getUserLocker();