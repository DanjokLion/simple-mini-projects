import * as fs from 'fs';
import * as path from 'path';
import { Workbook } from 'exceljs'

let workbook = new Workbook();
let worksheet = workbook.addWorksheet('Deal Uids');
worksheet.columns = [
    {header: 'DealUid', key: 'dealUid'}
]

const dirPath = path.resolve(__dirname);

fs.readdir(dirPath, (err, files) => {
    if (err) {
        console.error('Не удалось прочитать дир:', err);
        return;
    }

    const jsonFiles = files.filter(file => path.extname(file) === '.json');

    let dealUidCount = 0;
    let allUid = 0
    let dealSet = new Set<string>()

    // jsonFiles.forEach(file => {
    let fileReadPromises = jsonFiles.map(file => {
        return new Promise((resolve, reject) => {
            fs.readFile(path.join(dirPath, file), 'utf8', (err, data) => {
                if(err) {
                    console.error(`Не удалось прочитать файл ${file}:`, err);
                    reject(err);
                } else {
                    const jsonData = JSON.parse(data);

                    const countDealUid = (obj:any) => {
                        for (let key in obj) {
                            if (typeof obj[key] === 'object' && obj[key] !== null) {
                                countDealUid(obj[key]);
                            } else if (key === 'dealUid') {
                                dealUidCount++;
                                allUid++;
                                dealSet.add(obj[key]);
                                worksheet.addRow({file: file, dealUid: obj[key]});
                            }
                        }
                    }
                    
                    countDealUid(jsonData)
                    
                    console.log(`Кол-во dealUid в ${file}: ${dealUidCount}`)
                    resolve(null);
                }
            });
        });
    });


    Promise.all(fileReadPromises)
        .then(() => {
            let dealArray = Array.from(dealSet);
            dealArray.forEach((element, index) => {
                worksheet.getCell(`A${index + 1}`).value = element;
            })
            
            workbook.xlsx.writeFile('DealUids.xlsx')
                .then(() => console.log(`Excel файл сохранен, все dealUid с ошибками ${allUid}, Длинна Массива ${dealArray.length}`))
                .catch(err => console.error('Ошибка при сохранении', err));
    
        })
        .catch(err => console.log('Ошибка при чтении файлов', err))
    })
    
