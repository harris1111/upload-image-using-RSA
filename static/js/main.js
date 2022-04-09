function getRndInteger(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}
function gcd(a, b) {
    if (b === 0) {
        return a;
    } else {
        return gcd(b, a % b);
    }
}
function isPrime(n) {
    if (n <= 1) return false;

    for (let i = 2; i < n; i++)
        if (n % i == 0)
            return false;
    return true;
}
function getPrimeInt() {
    var p = getRndInteger(100, 1000);
    if (isPrime(p) === false) {
        return getPrimeInt();
    }
    return p;
}
function getQ(p) {
    var q = getPrimeInt();
    if (q === p) {
        return getQ();
    }
    return q;
}
function getE(phi) {
    while (true) {
        e = getRndInteger(2, phi);
        if (gcd(e, phi) === 1) {
            return e;
        }
    }
}
window.onload = function () {
    document.getElementById("btn-refresh").onclick = function () {
        var p = getPrimeInt();
        var q = getQ();
        var n = p * q;
        var phi = (p - 1) * (q - 1);
        var e = getE(phi);
        document.getElementById("random_n").innerHTML = "N = " + n;
        document.getElementById("random_e").innerHTML = "E = " + e;
    }
}