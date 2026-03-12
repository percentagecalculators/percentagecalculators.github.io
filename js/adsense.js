(function () {
    'use strict';

    var ADS = [
        {id: 'ad-header', slot: '3575522428'},
        {id: 'ad-body1',  slot: '2877013843'},
        {id: 'ad-body2',  slot: '3843445306'}
    ];

    function injectAd(config) {
        var container = document.getElementById(config.id);
        if (!container) return;

        var ins = document.createElement('ins');
        ins.className = 'adsbygoogle';
        ins.style.display = 'block';
        ins.setAttribute('data-ad-client', 'ca-pub-5426315045205785');
        ins.setAttribute('data-ad-slot', config.slot);
        ins.setAttribute('data-ad-format', 'auto');
        ins.setAttribute('data-full-width-responsive', 'true');

        container.appendChild(ins);
        (window.adsbygoogle = window.adsbygoogle || []).push({});
    }

    document.addEventListener('DOMContentLoaded', function () {
        ADS.forEach(injectAd);
    });
}());
