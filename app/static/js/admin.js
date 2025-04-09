function fetchAdminLockers() {
    const token = localStorage.getItem('access_token');
    fetch('/admin/lockers', {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => response.json())
    .then(data => {
        const lockerTableBody = document.querySelector('#adminLockerTable tbody');
        lockerTableBody.innerHTML = '';
        data.forEach(locker => {
            const row = document.createElement('tr');
            row.innerHTML = `<td>${locker.name}</td><td>${locker.locker_number}</td><td>${locker.firstName}</td><td>${locker.lastName}</td><td><button onclick="confirmDelete(${locker.id})">Delete</button></td>`;
            lockerTableBody.appendChild(row);
        });
    }).catch(error => {
        console.error("Error fetching lockers:", error);
    });
}

function confirmDelete(lockerID) {
    if (confirm("Are you sure you want to delete this locker assignment?")) {
        deleteLocker(lockerID);
    }
}

function deleteLocker(lockerID) {
    const token = localStorage.getItem('access_token');
    fetch('/admin/lockers/delete', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ locker_id: lockerID })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        fetchAdminLockers();
    }).catch(error => {
        console.error("Error deleting locker:", error);
    });
}

fetchAdminLockers();