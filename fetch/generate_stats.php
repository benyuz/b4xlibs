<?php
$outputDir = __DIR__ . '/../docs/data/';
file_put_contents('php://stderr', "📁 输出目录: " . $outputDir . "\n");
file_put_contents('php://stderr', "📁 脚本目录: " . __DIR__ . "\n");
file_put_contents('php://stderr', "📁 当前工作目录: " . getcwd() . "\n");

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
        'ranking' => array_slice($authors, 0, 20)
    ]
];

if (count($allLibraries) === 0) {
    file_put_contents('php://stderr', "⚠️ 没有数据文件，生成空统计\n");
}

$existingFile = $outputDir . 'stats.json';
$needsUpdate = true;

if (file_exists($existingFile)) {
    $existingStats = json_decode(file_get_contents($existingFile), true) ?: [];
    $existingData = $existingStats;
    $newData = $stats;
    unset($existingData['last_update'], $newData['last_update']);
    
    if (json_encode($existingData) === json_encode($newData)) {
        $needsUpdate = false;
    }
}

if ($needsUpdate) {
    file_put_contents($existingFile, json_encode($stats, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT));
    file_put_contents('php://stderr', "✅ 统计信息生成成功，总库数: " . $stats['total_libraries'] . "\n");
} else {
    file_put_contents('php://stderr', "✅ 统计信息无变化，跳过写入\n");
}
?>