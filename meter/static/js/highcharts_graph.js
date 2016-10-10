var chart;
var time_period;
var graph_type;
var chart_title = {'year': 'Consumo do último ano',
                   'month': 'Consumo dos últimos 30 dias',
                   'recent': 'Consumo da última hora'};
var chart_series = {'electricity': [{
                                        name: 'Corrente',
                                        data: []
                                    },
                                    {
                                        name: 'Tensão',
                                        data: []
                                    },
                                    {
                                        name: 'Potência',
                                        data: []
                                    }
                                   ],
                    'water': [{
                                name: 'Litros',
                                data: []
                              },
                              {
                                name: 'Metros Cúbicos',
                                data: []
                              }
                             ]
                    };

function get_graph_type(){
    var href = $(location).attr('href');
    if ((index = href.indexOf("meter/")) >= 0)
    {
        var index = index + 6;  // ignore the 'meter/' part of the string
        var page = href.substring(index, href.length).split("/");   // Returns array with 1 empty string, if string is empty
        if (page.length > 1){
            graph_type = page[0];
            switch(page[0]){
                case "electricity":
                    time_period = page[1];
                    break;
                case "water":
                    time_period = page[1];
                    break;
            }
        }
    }
}

function requestData() {
    $.ajax({
        url: '/meter/'+graph_type+'/'+time_period+'/values/',
        success: function(data) {
            if ((typeof data != undefined) && (data.cost != undefined) && (data.cost.length > 0)) {
                $('.show-avg-data').toggle(true);
                $('.show-no-avg-data').toggle(false);

                if (graph_type == 'electricity'){
                    // Add points
                    chart.series[0].setData(data['current']);
                    chart.series[1].setData(data['voltage']);
                    chart.series[2].setData(data['power']);

                    $('#avg_c').html(data['avg_c']);
                    $('#avg_v').html(data['avg_v']);
                    $('#avg_p').html(data['avg_p']);
                }else if(graph_type == 'water'){
                    // Add points
                    chart.series[0].setData(data['liters']);
                    chart.series[1].setData(data['cubic_meters']);

                    $('#total_l').html(data['total_l']);
                    $('#total_m3').html(data['total_m3']);
                }
                $('#cost').html(data['cost'] + '€');
                chart.legend.group.show();
                chart.legend.box.show();
                chart.legend.display = true;
            }
            else{
                $('.show-avg-data').toggle(false);
                $('.show-no-avg-data').toggle(true);
                chart.legend.group.hide();
                chart.legend.box.hide();
                chart.legend.display = false;
            }

            // Call it again every one second
            setTimeout(requestData, 1000);
        },
        cache: false
    });
}

$(document).ready(function() {
    get_graph_type();

    Highcharts.setOptions({
        lang: {noData: "Não existem dados a apresentar :("},
        global: {
            timezoneOffset: -60
        }
    });

    switch(time_period){
        case 'year':
            Highcharts.setOptions({
                xAxis: {
                    categories: ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez']
                },
            });
            switch(graph_type){
                case 'electricity':
                    Highcharts.setOptions({
                        tooltip: {
                            shared: false,
                            formatter: function(){
                                var text = '';
                                text += "<strong>" + this.x + "</strong><br />";
                                if(this.series.name == 'Corrente') {
                                    text += this.y + "A";
                                }
                                else if(this.series.name == 'Tensão') {
                                    text += this.y + "V";
                                }
                                if(this.series.name == 'Potência') {
                                    text += this.y + "W";
                                }
                                return text;
                            }
                        }
                    });
                    break;

                case 'water':
                    Highcharts.setOptions({
                        tooltip: {
                            shared: false,
                            formatter: function(){
                                var text = '';
                                text += "<strong>" + this.x + "</strong><br />";
                                if(this.series.name == 'Litros') {
                                    text += this.y + "l";
                                }
                                else if(this.series.name == 'Metros Cúbicos') {
                                    text += this.y + "m³";
                                }
                                return text;
                            }
                        }
                    });
                    break;
            }
            break;

        case 'month':
            Highcharts.setOptions({
                xAxis: {
                    type: 'datetime',
                },
            });
            switch(graph_type){
                case 'electricity':
                    Highcharts.setOptions({
                        tooltip: {
                            shared: false,
                            formatter: function(){
                                var text = '';
                                var options = { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' };
                                date = new Date(this.x).toLocaleDateString('pt-PT', options);
                                text = "<strong>"+date+"</strong><br />"
                                if(this.series.name == 'Corrente') {
                                    text += this.y + "A";
                                }
                                else if(this.series.name == 'Tensão') {
                                    var options = { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' };
                                    date = new Date(this.x).toLocaleDateString('pt-PT', options);
                                    text = "<strong>"+date+"</strong><br />"
                                    text += this.y + "V";
                                }
                                if(this.series.name == 'Potência') {
                                    text += this.y + "W";
                                }
                                return text;
                            }
                        }
                    });
                    break;

                case 'water':
                    Highcharts.setOptions({
                        tooltip: {
                            shared: false,
                            formatter: function(){
                                var text = '';
                                var options = { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' };
                                date = new Date(this.x).toLocaleDateString('pt-PT', options);
                                text = "<strong>"+date+"</strong><br />"
                                if(this.series.name == 'Litros') {
                                    text += this.y + "l";
                                }
                                else if(this.series.name == 'Metros Cúbicos') {
                                    text += this.y + "m³";
                                }
                                return text;
                            }
                        }
                    });
                    break;
            }
            break;

        case 'recent':
            Highcharts.setOptions({
                xAxis: {
                    type: 'datetime',
                    labels: {
                        format: '{value:%H:%M:%S}'
                    }
                }
            });
            switch(graph_type){
                case 'electricity':
                    Highcharts.setOptions({
                        tooltip: {
                            shared: false,
                            formatter: function(){
                                var text = '';
                                date = new Date(this.x);
                                text = "<strong>Hora: "+date.getHours()+"h"+date.getMinutes()+"m"+date.getSeconds()+"s</strong><br />";
                                if(this.series.name == 'Corrente') {
                                    text += this.y + "A";
                                }
                                else if(this.series.name == 'Tensão') {
                                    text += this.y + "V";
                                }
                                if(this.series.name == 'Potência') {
                                    text += this.y + "W";
                                }
                                return text;
                            }
                        }
                    });
                    break;
                case 'water':
                    Highcharts.setOptions({
                        tooltip: {
                            shared: false,
                            formatter: function(){
                                var text = '';
                                date = new Date(this.x);
                                text = "<strong>Hora: "+date.getHours()+"h"+date.getMinutes()+"m"+date.getSeconds()+"s</strong><br />";
                                if(this.series.name == 'Litros') {
                                    text += this.y + "l";
                                }
                                else if(this.series.name == 'Metros Cúbicos') {
                                    text += this.y + "m³";
                                }
                                return text;
                            }
                        }
                    });
                    break;
            }
            break;
    }

    chart = new Highcharts.Chart({
        chart: {
            renderTo: 'graph-container',
            defaultSeriesType: 'column',
            events: {
                load: requestData
            }
        },
        title: {
            text: chart_title[time_period]
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'top',
            x: -70,
            y: 30,
            floating: true,
            backgroundColor: '#ffffff',
            borderWidth: 1
        },
        yAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            type: 'logarithmic',
            title: {
                text: 'Valores',
            }
        },
        series: chart_series[graph_type]
    });

    chart.legend.group.hide();
    chart.legend.box.hide();
    chart.legend.display = false;
});