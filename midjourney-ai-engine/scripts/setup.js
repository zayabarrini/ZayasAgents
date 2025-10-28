#!/usr/bin/env node

import { execSync } from 'child_process';
import { readFileSync, writeFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

console.log('🚀 Setting up Midjourney AI Engine...\n');

try {
  // Update package.json with current path
  const packagePath = join(__dirname, '..', 'package.json');
  const packageJson = JSON.parse(readFileSync(packagePath, 'utf8'));
  
  console.log('📦 Installing dependencies...');
  execSync('npm install', { stdio: 'inherit' });
  
  console.log('✅ Dependencies installed successfully!');
  
  console.log('\n🎉 Setup complete! Next steps:');
  console.log('   npm run dev     - Start development server');
  console.log('   npm run lint    - Run ESLint');
  console.log('   npm run format  - Format code with Prettier');
  console.log('\n📚 Recommended VSCode extensions have been configured.');
  
} catch (error) {
  console.error('❌ Setup failed:', error.message);
  process.exit(1);
}