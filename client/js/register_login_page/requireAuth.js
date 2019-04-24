function requireAuth(url, option, requireAuthCallback) {
    loaderFunc('show');
    fetch(url, option)
        .then(function (response) {
            return response;
        })
        .then(function (data) {
            setTimeout(loaderFunc, 0, 'hide');
            requireAuthCallback(data); // temporarily !!!
        })
        .catch(function (error) {
            console.log(error);
        });
}