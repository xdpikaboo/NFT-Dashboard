import React, { useEffect, useRef, useState } from 'react';
import { createChart } from 'lightweight-charts';
import { round } from '../../helper/utils';
import "../../css/Chart.css"

function TradingViewChart({ time, value, title, value2, value3, isNormalized, addListedCount, name }) {

    const [ref] = useState(useRef());

    const [anchorChart, setAnchorChart] = useState(null);
    const [areaSeries, setAreaSeries] = useState(null);
    const [lineSeries, setLineSeries] = useState(null);
    const [lineSeries2, setLineSeries2] = useState(null);

    const [data, setData] = useState([]);

    const [data2, setData2] = useState([]);

    const [data3, setData3] = useState([]);

    const OFFSET = 14400000;

    function timeToTz(d) {
        return Date.UTC(d.getFullYear(), d.getMonth(), d.getDate(), d.getHours(), d.getMinutes(), d.getSeconds(), d.getMilliseconds()) / 1000;
    }

    const min = Math.min(...value);
    const max = Math.max(...value);
    const delta = max - min;

    const min2 = value2 ? Math.min(...value2) : null;
    const max2 = value2 ? Math.max(...value2) : null;
    const delta2 = value2 ? max2 - min2 : null;

    const min3 = value3 ? Math.min(...value3) : null;
    const max3 = value3 ? Math.max(...value3) : null;
    const delta3 = value3 ? max3 - min3 : null;

    let filterValue = value.filter((e) => !(e === null || e === -1))
    let filterValue2 = value2 ? value2.filter((e) => !(e === null || e === -1)) : null;
    let filterValue3 = value3 ? value3.filter((e) => !(e === null || e === -1)) : null;

    useEffect(() => {
        let toolTip = document.createElement('div')
        toolTip.className = 'chart-legend'
        value2 && value3 && ref.current.appendChild(toolTip)

        const darkTheme = {
            chart: {
                layout: {
                    backgroundColor: '#1c1f26',
                    lineColor: '#2B2B43',
                    textColor: '#D9D9D9',
                },
                watermark: {
                    color: 'rgba(0, 0, 0, 0)',
                },
                crosshair: {
                    color: '#758696',
                },
                grid: {
                    vertLines: {
                        color: '#2B2B43',
                    },
                    horzLines: {
                        color: '#363C4E',
                    },
                },
            },
            series: {
                topColor: '#394990',
                bottomColor: 'rgba(112, 82, 64, 0)',
                lineColor: '#394990',
            },
        };

        const themesData = {
            Dark: darkTheme,
        };

        function syncToTheme(theme, op1, op2) {
            op1.applyOptions(themesData[theme].chart);
            op2.applyOptions(themesData[theme].series);
        }

        if (!ref.current || anchorChart) return;

        const newChart = createChart(ref.current, {
            width: value2 ? window.innerWidth / 2 : window.innerWidth / 2.8,
            height: value2 ? window.innerHeight / 2 : window.innerHeight / 3,
            timeScale: {
                timeVisible: true,
            },
        })
        const newAreaSeries = newChart.addAreaSeries({
        });

        const newLineSeries = value2 ? newChart.addLineSeries({
            color: "#46acb7",
        }) : null;

        const newLineSeries2 = value3 ? newChart.addLineSeries({
            color: "#fd3c99",
        }) : null;

        syncToTheme('Dark', newChart, newAreaSeries);

        value2 && value3 && newChart.subscribeCrosshairMove(function (param) {

            let sentiment = param.seriesPrices.get(newAreaSeries) ? round(param.seriesPrices.get(newAreaSeries) * delta + min) : round(filterValue[filterValue.length - 1]);
            let floorPrice = param.seriesPrices.get(newLineSeries) ? round(param.seriesPrices.get(newLineSeries) * delta2 + min2) : round(filterValue2[filterValue2.length - 1]);
            let listedCount = param.seriesPrices.get(newLineSeries2) ? round(param.seriesPrices.get(newLineSeries2) * delta3 + min3) : round(filterValue3[filterValue3.length - 1]);

            toolTip.innerHTML =
                `<div>` +
                name +
                '</div>' +
                `<div>` +
                `Sentiment: ` + sentiment +
                '</div>' +
                '<div>' +
                `Floor price: ◎ ` + floorPrice +
                '</div>' +
                '<div>' +
                `Listed count: ` + listedCount +
                '</div>'
        })

        newChart.timeScale().fitContent();
        setAnchorChart(newChart);
        setAreaSeries(newAreaSeries);
        setLineSeries(newLineSeries);
        setLineSeries2(newLineSeries2)

    }, [ref, anchorChart, name, isNormalized, addListedCount, title, value, value2, value3, filterValue, filterValue2, filterValue3, delta, delta2, delta3, min, min2, min3]);


    useEffect(() => {
        let zip = time.map((d, i) => {
            return [timeToTz((new Date((new Date(d)).getTime() + OFFSET))), value[i]];
        });

        zip = zip.filter((element) => !(element[1] === null || element[1] === -1))

        const dataDict = zip.map((element) => {
            return {
                time: element[0],
                value: isNormalized ? (element[1] - min) / delta : element[1]
            }
        })

        setData(dataDict)

        if (value2) {


            let zip2 = time.map((d, i) => {
                return [timeToTz((new Date((new Date(d)).getTime() + OFFSET))), value2[i]];
            });

            zip2 = zip2.filter((element) => !(element[1] === null || element[1] === -1))

            const dataDict2 = zip2.map((element) => {
                return {
                    time: element[0],
                    value: isNormalized === true ? (element[1] - min2) / delta2 : element[1]
                }
            })

            setData2(dataDict2)
        }

        if (value3) {

            if (addListedCount) {


                let zip3 = time.map((d, i) => {
                    return [timeToTz((new Date((new Date(d)).getTime() + OFFSET))), value3[i]];
                });

                zip3 = zip3.filter((element) => !(element[1] === null || element[1] === -1))

                const dataDict3 = zip3.map((element) => {
                    return {
                        time: element[0],
                        value: isNormalized === true ? (element[1] - min3) / delta3 : element[1]
                    }
                })

                setData3(dataDict3)
            }
            else {
                setData3([])
            }
        }
        // eslint-disable-next-line
    }, [isNormalized, addListedCount])

    useEffect(() => {

        if (data.length > 0) {
            areaSeries.setData(data);
            if (lineSeries) {
                lineSeries.setData(data2);
            }
            if (lineSeries2) {
                lineSeries2.setData(data3);
            }
        }
        // eslint-disable-next-line
    }, [data, data2, data3]);

    const generateTitle = () => {
        return title
    }

    return (
        <div style={{ marginBottom: "4vh" }}>
            <div style={{ fontSize: "1.5vw", marginBottom: "4vh", float: "left" }}>{generateTitle()}</div>
            <div ref={ref} style={{ position: "relative" }} />
        </div>
    );
}

export default TradingViewChart;


