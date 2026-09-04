(function () {
    'use strict';

    var ADS = [
        {id: 'ad-header', slot: '3575522428', responsive: true},
        {id: 'ad-body1',  slot: '2877013843', responsive: false},
        {id: 'ad-body2',  slot: '3843445306', responsive: false}
    ];

    function injectAd(config) {
        var container = document.getElementById(config.id);
        if (!container) return;

        var ins = document.createElement('ins');
        ins.className = 'adsbygoogle';
        ins.setAttribute('data-ad-client', 'ca-pub-5426315045205785');
        ins.setAttribute('data-ad-slot', config.slot);

        if (config.responsive) {
            var w = container.offsetWidth >= 728 ? '728px' : '300px';
            var h = container.offsetWidth >= 728 ? '90px' : '100px';
            ins.style.display = 'inline-block';
            ins.style.width = w;
            ins.style.height = h;
        } else {
            ins.style.display = 'inline-block';
            ins.style.width = '300px';
            ins.style.height = '250px';
        }

        container.appendChild(ins);
        (window.adsbygoogle = window.adsbygoogle || []).push({});
    }

    document.addEventListener('DOMContentLoaded', function () {
        ADS.forEach(injectAd);
    });
}());
