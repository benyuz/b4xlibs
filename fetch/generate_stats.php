<?php
$dataDir = __DIR__ . '/../site/data/';

$official = [];
$community = [];

if (file_exists($dataDir . 'official.json')) {
    $official = json_decode(file_get_contents($dataDir . 'official.json'), true) ?: [];
}
if (file_exists($dataDir . 'community.json')) {
    $community = json_decode(file_get_contents($dataDir . 'community.json'), true) ?: [];
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
        'ranking' => array_slice($authors, 0, 20)
    ]
];

if (count($allLibraries) === 0) {
    file_put_contents('php://stderr', "⚠️ 没有数据文件，生成空统计\n");
}

file_put_contents($dataDir . 'stats.json', json_encode($stats, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT));
file_put_contents('php://stderr', "✅ 统计信息生成成功，总库数: " . $stats['total_libraries'] . "\n");
?>