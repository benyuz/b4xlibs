<?php
$outputDir = __DIR__ . '/../docs/data/';

$official = [];
$community = [];

if (file_exists($outputDir . 'official.json')) {
    $official = json_decode(file_get_contents($outputDir . 'official.json'), true) ?: [];
}
if (file_exists($outputDir . 'community.json')) {
    $community = json_decode(file_get_contents($outputDir . 'community.json'), true) ?: [];
}

$allLibraries = array_merge($official, $community);
$authors = [];
foreach ($allLibraries as $lib) {
    if (!empty($lib['author'])) {
        $authors[$lib['author']] = ($authors[$lib['author']] ?? 0) + 1;
    }
}
arsort($authors);

$stats = [
    'last_update' => date('Y-m-d H:i:s'),
    'total_libraries' => count($allLibraries),
    'official_count' => count($official),
    'community_count' => count($community),
    'authors' => [
        'total' => count($authors),
        'ranking' => $authors
    ]
];

if (count($allLibraries) === 0) {
    file_put_contents('php://stderr', "⚠️ 没有数据文件，生成空统计\n");
}

file_put_contents($outputDir . 'stats.json', json_encode($stats, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT));
file_put_contents('php://stderr', "✅ 统计信息生成成功，总库数: " . $stats['total_libraries'] . "\n");
?>