// Morris.js Charts sample data for SB Admin template

$(function() {

    // Area Chart
    Morris.Area({
        element: 'protocol-chart',
        data: [{
            time: '2016-10-10 12:01:13.381941',
            http: 2666,
            arp: null,
            dns: 2647
        }, {
            time: '2010 Q2',
            http: 2778,
            arp: 2294,
            dns: 2441
        }, {
            time: '2010 Q3',
            http: 4912,
            arp: 1969,
            dns: 2501
        }, {
            time: '2010 Q4',
            http: 3767,
            arp: 3597,
            dns: 5689
        }, {
            time: '2011 Q1',
            http: 6810,
            arp: 1914,
            dns: 2293
        }, {
            time: '2011 Q2',
            http: 5670,
            arp: 4293,
            dns: 1881
        }, {
            time: '2011 Q3',
            http: 4820,
            arp: 3795,
            dns: 1588
        }, {
            time: '2011 Q4',
            http: 15073,
            arp: 5967,
            dns: 5175
        }, {
            time: '2012 Q1',
            http: 10687,
            arp: 4460,
            dns: 2028
        }, {
            time: '2012 Q2',
            http: 8432,
            arp: 5713,
            dns: 1791
        }],
        xkey: 'time',
        ykeys: ['http', 'arp', 'dns'],
        labels: ['HTTP', 'ARP', 'DNS'],
        pointSize: 3,
        hideHover: 'auto',
        resize: true
    });

    // Donut Chart
    Morris.Donut({
        element: 'morris-donut-chart',
        data: [{
            label: "naver.com",
            value: 122
        }, {
            label: "google.com",
            value: 340
        }, {
            label: "github.com",
            value: 210
        }, {
            label: "trello.com",
            value: 312
        }],
        resize: true
    });

    // Line Chart
    Morris.Line({
        // ID of the element in which to draw the chart.
        element: 'morris-line-chart',
        // Chart data records -- each entry in this array corresponds to a point on
        // the chart.
        data: [{
            d: '2012-10-01',
            visits: 802
        }, {
            d: '2012-10-02',
            visits: 783
        }, {
            d: '2012-10-03',
            visits: 820
        }, {
            d: '2012-10-04',
            visits: 839
        }, {
            d: '2012-10-05',
            visits: 792
        }, {
            d: '2012-10-06',
            visits: 859
        }, {
            d: '2012-10-07',
            visits: 790
        }, {
            d: '2012-10-08',
            visits: 1680
        }, {
            d: '2012-10-09',
            visits: 1592
        }, {
            d: '2012-10-10',
            visits: 1420
        }, {
            d: '2012-10-11',
            visits: 882
        }, {
            d: '2012-10-12',
            visits: 889
        }, {
            d: '2012-10-13',
            visits: 819
        }, {
            d: '2012-10-14',
            visits: 849
        }, {
            d: '2012-10-15',
            visits: 870
        }, {
            d: '2012-10-16',
            visits: 1063
        }, {
            d: '2012-10-17',
            visits: 1192
        }, {
            d: '2012-10-18',
            visits: 1224
        }, {
            d: '2012-10-19',
            visits: 1329
        }, {
            d: '2012-10-20',
            visits: 1329
        }, {
            d: '2012-10-21',
            visits: 1239
        }, {
            d: '2012-10-22',
            visits: 1190
        }, {
            d: '2012-10-23',
            visits: 1312
        }, {
            d: '2012-10-24',
            visits: 1293
        }, {
            d: '2012-10-25',
            visits: 1283
        }, {
            d: '2012-10-26',
            visits: 1248
        }, {
            d: '2012-10-27',
            visits: 1323
        }, {
            d: '2012-10-28',
            visits: 1390
        }, {
            d: '2012-10-29',
            visits: 1420
        }, {
            d: '2012-10-30',
            visits: 1529
        }, {
            d: '2012-10-31',
            visits: 1892
        }, ],
        // The name of the data record attribute that contains x-visitss.
        xkey: 'd',
        // A list of names of data record attributes that contain y-visitss.
        ykeys: ['visits'],
        // Labels for the ykeys -- will be displayed when you hover over the
        // chart.
        labels: ['Visits'],
        // Disables line smoothing
        smooth: false,
        resize: true
    });

    // Bar Chart
    Morris.Bar({
        element: 'morris-bar-chart',
        data: [{
            device: 'http',
            geekbench: 136
        }, {
            device: 'http 3G',
            geekbench: 137
        }, {
            device: 'http 3GS',
            geekbench: 275
        }, {
            device: 'http 4',
            geekbench: 380
        }, {
            device: 'http 4S',
            geekbench: 655
        }, {
            device: 'http 5',
            geekbench: 1571
        }],
        xkey: 'device',
        ykeys: ['geekbench'],
        labels: ['Geekbench'],
        barRatio: 0.4,
        xLabelAngle: 35,
        hideHover: 'auto',
        resize: true
    });


});
