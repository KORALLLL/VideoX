import { defineStyleConfig } from '@chakra-ui/react'

export const ButtonTheme = defineStyleConfig({
  baseStyle: {
    borderRadius: '7px',
    fontWeight: '700',
    background: 'lightblue.400',
    color: 'white',
    _hover: { background: 'lightblue.500', color: 'white' },
    _disabled: { color: 'gray.200', background: 'blue.300', opacity: 1 },
  },
  variants: {
    baseStyle: {
      background: 'lightblue.400',
      color: 'white',
      _hover: { background: 'lightblue.500', color: 'white' },
      _disabled: { color: 'gray.200', background: 'blue.300', opacity: 1 },
    },
    'start-training': {
      textAlign: 'left',
      background: 'blue.600',
      _hover: { background: 'blue.700' },
      color: 'white',
    },
    'skip-training': {
      border: '1px solid #559BED',
      background: 'white',
      _hover: { background: 'gray.100', color: 'blue.600' },
      color: 'blue.600',
    },
    'container-page': {
      background: 'lightblue.400',
      textAlign: 'center',
      _hover: { bg: 'lightblue.500', color: 'white' },
      color: 'white',
    },
    instruction: {
      w: '21px',
      h: '21px',
      background: 'white',
      border: '1px solid #559BED',
      textAlign: 'center',
      _hover: {
        background: 'white',
        color: 'blue.700',
        border: '1px solid #3576C2',
      },
      color: 'blue.600',
    },
    delete: {
      background: 'red.200',
      textAlign: 'center',
      _hover: {
        background: 'red.300',
        color: 'white',
      },
    },
  },
})
