project (
  'cc2540',
)

cc = find_program('sdcc')
ld = find_program('sdld')
ar = find_program('sdar')

c_args = [
  '-O0',
  '-mmcs51',
  '--model-medium',
  '--xram-loc 0x0000',
  '--xram-size 0x2000',
  '--iram-size 0x0100',
  '-DUART0',
  '-Wa,-glos',
  '-Wa,-p'
]

compiler = generator(
  cc,
  arguments: [
    c_args,
    '-o',
    '@OUTPUT@',
    '-c',
    '@INPUT@',
  ],
  output: '@BASENAME@.rel',
)

common = compiler.process(
  [
    'delay.c',
    'time.c',
    'uart.c',
    'usb.c',
    'usb_cdc_acm.c',
    'util.c',
  ],
)

blink = compiler.process('test_blink.c')

blink_test = custom_target(
  build_by_default: true,
  command: [cc, c_args, '-o', '@OUTPUT@', '@INPUT@'],
  input: [blink, common],
  output: 'blink.bin',
)