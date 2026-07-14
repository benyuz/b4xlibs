<?php
$csvUrl = 'https://docs.google.com/spreadsheets/d/1qFvc3Q70RriJS3m_ywBoJvZ47gSTVAuN_X04SI0_XBw/export?format=csv&gid=0';

$csv = file_get_contents($csvUrl);
if ($csv === false) {
    file_put_contents('php://stderr', "❌ 抓取官方库CSV失败\n");
    exit(1);
}

$lines = explode("\n", $csv);
$libraries = [];
$headers = null;

foreach ($lines as $line) {
    $data = str_getcsv($line);
    if (empty($data) || empty($data[0])) continue;
    if ($headers === null) {
        $headers = $data;
        continue;
    }
    if ($data[0] === 'Library Name') continue;
    
    $lib = [
        'name' => trim($data[0] ?? ''),
        'desc' => trim($data[1] ?? ''),
        'b4a' => trim($data[2] ?? ''),
        'b4i' => trim($data[3] ?? ''),
        'b4j' => trim($data[4] ?? ''),
        'b4r' => trim($data[5] ?? ''),
        'version' => trim($data[6] ?? ''),
        'date' => trim($data[7] ?? ''),
        'author' => trim($data[8] ?? ''),
        'link' => trim($data[10] ?? '')
    ];
    
    if (empty($lib['name'])) continue;
    
    $tags = [];
    if (!empty($lib['b4a'])) $tags[] = 'B4A';
    if (!empty($lib['b4i'])) $tags[] = 'B4I';
    if (!empty($lib['b4j'])) $tags[] = 'B4J';
    if (!empty($lib['b4r'])) $tags[] = 'B4R';
    $lib['tags'] = $tags;
    unset($lib['b4a'], $lib['b4i'], $lib['b4j'], $lib['b4r']);
    
    $libraries[] = $lib;
}

if (count($libraries) < 10) {
    file_put_contents('php://stderr', "❌ 官方库数据异常，仅 " . count($libraries) . " 条\n");
    exit(1);
}

$json = json_encode($libraries, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
$outputDir = __DIR__ . '/../site/data/';
if (!is_dir($outputDir)) mkdir($outputDir, 0755, true);

file_put_contents($outputDir . 'official.json', $json);
file_put_contents($outputDir . 'official.json.gz', gzencode($json, 9));

file_put_contents('php://stderr', "✅ 官方库更新成功，共 " . count($libraries) . " 条\n");
?>