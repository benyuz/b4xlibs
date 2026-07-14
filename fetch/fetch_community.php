<?php
$htmlUrl = 'https://www.dropbox.com/s/4punyxbwek8oc8o/b4xgoodies.html?dl=1';

$ctx = stream_context_create([
    'http' => [
        'user_agent' => 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'follow_location' => true,
        'max_redirects' => 5,
        'timeout' => 30
    ],
    'ssl' => [
        'verify_peer' => false,
        'verify_peer_name' => false
    ]
]);

$html = file_get_contents($htmlUrl, false, $ctx);
if ($html === false) {
    file_put_contents('php://stderr', "❌ 抓取社区库HTML失败\n");
    exit(1);
}

$dom = new DOMDocument();
libxml_use_internal_errors(true);
$dom->loadHTML($html, LIBXML_NOERROR | LIBXML_NOWARNING);
libxml_clear_errors();

$xpath = new DOMXPath($dom);
$tableRows = $xpath->query('//table/tr');

$libraries = [];
for ($i = 3; $i < $tableRows->length; $i++) {
    $row = $tableRows->item($i);
    $cells = $row->getElementsByTagName('td');
    if ($cells->length < 11) continue;
    
    $data = [];
    foreach ($cells as $cell) {
        $data[] = trim($cell->textContent);
    }
    
    if (empty($data[3])) continue;
    if (strtolower($data[1] ?? '') !== 'library') continue;
    
    $b4what = strtolower($data[0] ?? '');
    $tags = [];
    if ($b4what === 'b4x') $tags = ['B4A', 'B4I', 'B4J', 'B4R'];
    elseif ($b4what === 'b4a') $tags = ['B4A'];
    elseif ($b4what === 'b4i') $tags = ['B4I'];
    elseif ($b4what === 'b4j') $tags = ['B4J'];
    elseif ($b4what === 'b4r') $tags = ['B4R'];
    
    $libraries[] = [
        'name' => trim($data[3] ?? ''),
        'desc' => trim($data[8] ?? ''),
        'tags' => $tags,
        'version' => trim(preg_replace('/^[vV]/', '', $data[5] ?? '')),
        'date' => trim($data[6] ?? ''),
        'author' => trim($data[4] ?? ''),
        'link' => trim($data[9] ?? '')
    ];
}

if (count($libraries) < 10) {
    file_put_contents('php://stderr', "❌ 社区库数据异常，仅 " . count($libraries) . " 条\n");
    exit(1);
}

$json = json_encode($libraries, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
$outputDir = __DIR__ . '/../docs/data/';
file_put_contents('php://stderr', "📁 输出目录: " . $outputDir . "\n");
file_put_contents('php://stderr', "📁 脚本目录: " . __DIR__ . "\n");
file_put_contents('php://stderr', "📁 当前工作目录: " . getcwd() . "\n");
if (!is_dir($outputDir)) mkdir($outputDir, 0755, true);

file_put_contents($outputDir . 'community.json', $json);
file_put_contents($outputDir . 'community.json.gz', gzencode($json, 9));

file_put_contents('php://stderr', "✅ 社区库更新成功，共 " . count($libraries) . " 条\n");
?>