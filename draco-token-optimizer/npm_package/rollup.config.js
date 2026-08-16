/** @type {import('rollup').RollupConfig} */
const resolve = require('@rollup/plugin-node-resolve');
const commonjs = require('@rollup/plugin-commonjs');
const json = require('@rollup/plugin-json');
import typescript from '@rollup/plugin-typescript';
const sass = require('rollup-plugin-sass');
const postcss = require('rollup-plugin-postcss');

const production = process.env.ROLLUP_WORKER_ENV === 'production';

export default [
  {
    input: 'src/index.ts',
    output: [
      {
        file: 'dist/draco.umd.js',
        name: 'Draco',
        format: 'umd',
        globals: {
          'onnxruntime-web': 'ONNXRuntime',
          'rank-bm25': 'BM25',
          'pegasus-js': 'Pegasus',
        },
        sourcemap: !production,
      },
      {
        file: 'dist/draco.esm.js',
        format: 'esm',
        sourcemap: !production,
      },
    ],
    plugins: [
      resolve(),
      commonjs(),
      json(),
      typescript({
        tsconfig: './tsconfig.json',
        sourceMap: !production,
      }),
      sass({
        output: 'dist/styles.css',
      }),
      postcss(),
    ],
    watch: {
      clearScreen: false,
    },
  },

  {
    input: 'src/types.d.ts',
    output: [
      {
        file: 'dist/draco.d.ts',
        format: 'types',
      },
    ],
    plugins: [typescript()],
  },
];