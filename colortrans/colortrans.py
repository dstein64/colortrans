import argparse
import sys

import numpy as np
import os
from PIL import Image


METHODS = ('cwct', 'lhm', 'pccm', 'reinhard')

version_txt = os.path.join(os.path.dirname(__file__), 'version.txt')
with open(version_txt, 'r') as f:
    __version__ = f.read().strip()


def transfer_cwct(content, reference):
    """Transfers colors from a reference image to a content image using
    channel-wise color transfer.

    content: NumPy array (HxWxC)
    reference: NumPy array (HxWxC)
    """
    # Convert HxWxC image to a (H*W)xC matrix.
    shape = content.shape
    assert len(shape) == 3
    content = content.reshape(-1, shape[-1]).astype(np.float32)
    reference = reference.reshape(-1, shape[-1]).astype(np.float32)

    mu_content = np.mean(content, axis=0)
    mu_reference = np.mean(reference, axis=0)

    std_source = np.std(content, axis=0)
    std_target = np.std(reference, axis=0)

    result = content - mu_content
    result *= std_target
    result /= std_source
    result += mu_reference
    # Restore image dimensions.
    result = result.reshape(shape).clip(0, 255).round().astype(np.uint8)

    return result


def transfer_lhm(content, reference):
    """Transfers colors from a reference image to a content image using the
    Linear Histogram Matching.

    content: NumPy array (HxWxC)
    reference: NumPy array (HxWxC)
    """
    # Convert HxWxC image to a (H*W)xC matrix.
    shape = content.shape
    assert len(shape) == 3
    content = content.reshape(-1, shape[-1]).astype(np.float32)
    reference = reference.reshape(-1, shape[-1]).astype(np.float32)

    def matrix_sqrt(X):
        eig_val, eig_vec = np.linalg.eig(X)
        return eig_vec.dot(np.diag(np.sqrt(eig_val))).dot(eig_vec.T)

    mu_content = np.mean(content, axis=0)
    mu_reference = np.mean(reference, axis=0)

    cov_content = np.cov(content, rowvar=False)
    cov_reference = np.cov(reference, rowvar=False)

    result = matrix_sqrt(cov_reference)
    result = result.dot(np.linalg.inv(matrix_sqrt(cov_content)))
    result = result.dot((content - mu_content).T).T
    result = result + mu_reference
    # Restore image dimensions.
    result = result.reshape(shape).clip(0, 255).round().astype(np.uint8)

    return result


def transfer_pccm(content, reference):
    """Transfers colors from a reference image to a content image using
    Principal Component Color Matching.

    content: NumPy array (HxWxC)
    reference: NumPy array (HxWxC)
    """
    # Convert HxWxC image to a (H*W)xC matrix.
    shape = content.shape
    assert len(shape) == 3
    content = content.reshape(-1, shape[-1]).astype(np.float32)
    reference = reference.reshape(-1, shape[-1]).astype(np.float32)

    mu_content = np.mean(content, axis=0)
    mu_reference = np.mean(reference, axis=0)

    cov_content = np.cov(content, rowvar=False)
    cov_reference = np.cov(reference, rowvar=False)

    eigval_content, eigvec_content = np.linalg.eig(cov_content)
    eigval_reference, eigvec_reference = np.linalg.eig(cov_reference)

    scaling = np.diag(np.sqrt(eigval_reference / eigval_content))
    transform = eigvec_reference.dot(scaling).dot(eigvec_content.T)
    result = (content - mu_content).dot(transform.T) + mu_reference
    # Restore image dimensions.
    result = result.reshape(shape).clip(0, 255).round().astype(np.uint8)

    return result


def transfer_reinhard(content, reference):
    """Transfers colors from a reference image to a content image using the
    technique from Reinhard et al.

    content: NumPy array (HxWxC)
    reference: NumPy array (HxWxC)
    """
    # Convert HxWxC image to a (H*W)xC matrix.
    shape = content.shape
    assert len(shape) == 3
    content = content.reshape(-1, shape[-1]).astype(np.float32)
    reference = reference.reshape(-1, shape[-1]).astype(np.float32)

    m1 = np.array([
        [0.3811, 0.1967, 0.0241],
        [0.5783, 0.7244, 0.1288],
        [0.0402, 0.0782, 0.8444],
    ])

    m2 = np.array([
        [0.5774, 0.4082, 0.7071],
        [0.5774, 0.4082, -0.7071],
        [0.5774, -0.8165, 0.0000],
    ])

    m3 = np.array([
        [0.5774, 0.5774, 0.5774],
        [0.4082, 0.4082, -0.8165],
        [0.7071, -0.7071, 0.0000],
    ])

    m4 = np.array([
        [4.4679, -1.2186, 0.0497],
        [-3.5873, 2.3809, -0.2439],
        [0.1193, -0.1624, 1.2045],
    ])

    # Avoid log of 0. Clipping is used instead of adding epsilon, to avoid
    # taking a log of a small number whose very low output distorts the results.
    # WARN: This differs from the Reinhard paper, where no adjustment is made.
    lab_content = np.log10(np.maximum(1.0, content.dot(m1))).dot(m2)
    lab_reference = np.log10(np.maximum(1.0, reference.dot(m1))).dot(m2)

    mu_content = lab_content.mean(axis=0)
    mu_reference = lab_reference.mean(axis=0)

    std_source = np.std(content, axis=0)
    std_target = np.std(reference, axis=0)

    result = lab_content - mu_content
    result *= std_target
    result /= std_source
    result += mu_reference
    result = (10 ** result.dot(m3)).dot(m4)
    # Restore image dimensions.
    result = result.reshape(shape).clip(0, 255).round().astype(np.uint8)

    return result


# ************************************************************
# * Command Line Interface
# ************************************************************

def parse_args(argv):
    parser = argparse.ArgumentParser(
        prog='colortrans',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # Optional arguments
    parser.add_argument(
        '--method', default='lhm', choices=METHODS,
        help='Algorithm to use for color transfer.')

    # Required arguments
    parser.add_argument('content', help='Path to content image (qualitative appearance).')
    parser.add_argument('reference', help='Path to reference image (desired colors).')
    parser.add_argument('output', help='Path to output image.')

    args = parser.parse_args(argv[1:])

    return args


def main(argv=sys.argv):
    args = parse_args(argv)
    content_img = Image.open(args.content).convert('RGB')
    # The slicing is to remove transparency channels if they exist.
    content = np.array(content_img)[:, :, :3]
    reference_img = Image.open(args.reference).convert('RGB')
    reference = np.array(reference_img)[:, :, :3]
    transfer = globals()[f'transfer_{args.method}']
    output = transfer(content, reference)
    Image.fromarray(output).save(args.output)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
